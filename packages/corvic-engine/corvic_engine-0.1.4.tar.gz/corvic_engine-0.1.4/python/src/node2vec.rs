use numpy::ndarray::{Array1, ArrayView1, ArrayViewMut1, ArrayViewMut2};
use numpy::{PyArrayLike2, TypeMustMatch};
use pyo3::exceptions::{PyOverflowError, PyValueError};
use pyo3::prelude::*;
use rayon::prelude::*;
use std::cell::RefCell;
use std::cmp::{max, min};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use thread_local::ThreadLocal;

use crate::datarace::UnsafeSync;
use crate::fastfn;
use crate::graph::{self, CSRGraph, NodeT};
use crate::random::FastRandom;

fn saxpy(a: f32, x: &ArrayView1<'_, f32>, y: &mut ArrayViewMut1<'_, f32>) {
    let n = x.len();
    unsafe {
        for i in 0..n {
            *y.uget_mut(i) = a * x.uget(i) + y.uget(i);
        }
    }
}

#[allow(clippy::too_many_arguments)]
fn train_node2vec_sentence(
    num_negative: usize,
    total_words: NodeT,
    embeddings: &UnsafeSync<ArrayViewMut2<f32>>,
    hidden_layer: &UnsafeSync<ArrayViewMut2<f32>>,
    current_word: NodeT,
    context_word: NodeT,
    alpha: f32,
    work: &mut ArrayViewMut1<f32>,
    random: &mut FastRandom,
) {
    work.fill(0.);

    let embeddings_array = unsafe { embeddings.uget() };
    let hidden_layer_array = unsafe { hidden_layer.uget() };

    for count_neg in 0..num_negative + 1 {
        let mut target_index = current_word as usize;
        let mut label = 1.;
        if count_neg != 0 {
            target_index = random.next_i32(total_words.try_into().unwrap()) as usize;

            label = 0.;
            if target_index == (current_word as usize) {
                continue;
            }
        }

        let error = embeddings_array
            .row(context_word as usize)
            .dot(&hidden_layer_array.row(target_index));

        match fastfn::sigmoid(error) {
            None => continue,
            Some(f) => {
                let g = (label - f) * alpha;

                saxpy(g, &hidden_layer_array.row(target_index), work);
                saxpy(
                    g,
                    &embeddings_array.row(context_word as usize),
                    &mut hidden_layer_array.row_mut(target_index),
                );
            }
        }
    }

    saxpy(
        1.,
        &work.view(),
        &mut embeddings_array.row_mut(context_word as usize),
    );
}

/// Trains a batch of data for node2vec
#[allow(clippy::too_many_arguments)]
fn train_node2vec_batch_array(
    graph: &CSRGraph,
    nodes: ArrayView1<NodeT>,
    alpha: f64,
    params: &Node2VecParams,
    embeddings: &UnsafeSync<ArrayViewMut2<f32>>,
    hidden_layer: &UnsafeSync<ArrayViewMut2<f32>>,
    mut work: ArrayViewMut1<f32>,
    random: &mut FastRandom,
) {
    let mut walk = Vec::with_capacity(params.max_walk_length);

    for node in nodes.iter() {
        graph::random_walk(
            graph,
            *node,
            params.max_walk_length,
            params.p as f32,
            params.q as f32,
            random,
            &mut walk,
        );

        for cur in 0..walk.len() {
            let window_delta = random.next_i32(params.window);
            let begin = max(cur as i32 - params.window + window_delta, 0) as usize;
            let end = min(
                cur as i32 + params.window + 1 - window_delta,
                walk.len() as i32,
            ) as usize;

            for context in begin..end {
                if cur == context {
                    continue;
                }
                train_node2vec_sentence(
                    params.num_negative,
                    graph.num_nodes(),
                    embeddings,
                    hidden_layer,
                    *walk.get(cur).unwrap(),
                    *walk.get(context).unwrap(),
                    alpha as f32,
                    &mut work,
                    random,
                )
            }
        }
    }
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct Node2VecParams {
    #[pyo3(get)]
    p: f64,
    #[pyo3(get)]
    q: f64,
    #[pyo3(get)]
    start_alpha: f64,
    #[pyo3(get)]
    end_alpha: f64,
    #[pyo3(get)]
    window: i32,
    #[pyo3(get)]
    batch_size: usize,
    #[pyo3(get)]
    max_walk_length: usize,
    #[pyo3(get)]
    num_negative: usize,
    #[pyo3(get)]
    workers: Option<usize>,
}

#[pymethods]
impl Node2VecParams {
    #[allow(clippy::too_many_arguments)]
    #[new]
    #[pyo3(signature = (*, p, q, start_alpha, end_alpha, window, batch_size, max_walk_length, num_negative, workers))]
    fn new(
        p: f64,
        q: f64,
        start_alpha: f64,
        end_alpha: f64,
        window: i32,
        batch_size: usize,
        max_walk_length: usize,
        num_negative: usize,
        workers: Option<usize>,
    ) -> Self {
        Self {
            p,
            q,
            start_alpha,
            end_alpha,
            window,
            batch_size,
            max_walk_length,
            num_negative,
            workers,
        }
    }
}

#[pyfunction]
#[pyo3(signature = (*, graph, params, embeddings, hidden_layer, next_random))]
pub fn train_node2vec_epoch(
    graph: &CSRGraph,
    params: Node2VecParams,
    embeddings: PyArrayLike2<f32, TypeMustMatch>,
    hidden_layer: PyArrayLike2<f32, TypeMustMatch>,
    next_random: u64,
) -> PyResult<()> {
    if graph.num_nodes() == 0 {
        return Ok(());
    }

    if graph.num_nodes() as u64 > i32::MAX as u64 {
        return Err(PyOverflowError::new_err(
            "graphs larger than i32 not yet supported",
        ));
    }

    let mut random = FastRandom::new(next_random);

    let mut permutation = Vec::<NodeT>::with_capacity(graph.num_nodes() as usize);
    (0..graph.num_nodes()).for_each(|v| {
        permutation.push(v);
    });
    random.permute(permutation.as_mut_slice());

    let child_seed = ((random.next(32) as u64) << 32) | random.next(32) as u64;

    let tld = ThreadLocal::<RefCell<Array1<f32>>>::new();

    let mut embeddings_array = unsafe { embeddings.as_array_mut() };
    let mut hidden_layer_array = unsafe { hidden_layer.as_array_mut() };

    let dim = hidden_layer_array.ncols();
    // Round up
    let total_batches =
        (graph.num_nodes() + params.batch_size as u32 - 1) / params.batch_size as u32;

    let unsafe_embeddings_array = UnsafeSync::from(&mut embeddings_array);
    let unsafe_hidden_layer_array = UnsafeSync::from(&mut hidden_layer_array);

    let counter = Arc::new(AtomicUsize::new(0));

    let func = || {
        permutation.par_chunks(params.batch_size).for_each(|batch| {
            let count = counter.fetch_add(1, Ordering::SeqCst);
            let work = tld.get_or(|| RefCell::new(Array1::<f32>::zeros(dim)));
            let mut random = FastRandom::new(child_seed + count as u64);

            let ratio = count as f64 / total_batches as f64;
            let alpha = params.start_alpha - (params.start_alpha - params.end_alpha) * ratio;

            train_node2vec_batch_array(
                graph,
                ArrayView1::from(&batch),
                alpha,
                &params,
                &unsafe_embeddings_array,
                &unsafe_hidden_layer_array,
                work.borrow_mut().view_mut(),
                &mut random,
            )
        });
    };

    match params.workers {
        Some(workers) => match rayon::ThreadPoolBuilder::new().num_threads(workers).build() {
            Ok(pool) => {
                pool.install(func);
                Ok(())
            }
            Err(err) => Err(PyValueError::new_err(err.to_string())),
        },
        None => {
            func();
            Ok(())
        }
    }
}
