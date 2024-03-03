use numpy::PyReadonlyArray2;
use pyo3::prelude::*;

pub type NodeT = u32;
pub type EdgeT = u64;

use crate::random::FastRandom;

#[pyclass]
pub struct CSRGraph {
    neighbors: Vec<NodeT>,
    outs: Vec<EdgeT>,
}

impl CSRGraph {
    pub fn new(num_nodes: usize, num_edges: usize) -> Self {
        Self {
            neighbors: vec![0; num_edges],
            outs: vec![0; num_nodes + 1],
        }
    }

    fn out_neighbors_slice(&self, src: NodeT) -> &[NodeT] {
        let start = self.outs[src as usize];
        let end = self.outs[(src + 1) as usize];
        &self.neighbors[start as usize..end as usize]
    }

    fn out_neighbors_slice_mut(&mut self, src: NodeT) -> &mut [NodeT] {
        let start = self.outs[src as usize];
        let end = self.outs[(src + 1) as usize];
        &mut self.neighbors[start as usize..end as usize]
    }
}

#[pymethods]
impl CSRGraph {
    pub fn num_nodes(&self) -> NodeT {
        let len = self.outs.len();
        if len == 0 {
            0
        } else {
            (len - 1) as NodeT
        }
    }

    pub fn has_edge(&self, src: NodeT, dst: NodeT) -> bool {
        return self.out_neighbors_slice(src).binary_search(&dst).is_ok();
    }
}

#[pyfunction]
#[pyo3(text_signature = "(*, edges, directed)")]
pub fn csr_from_edges(edges: PyReadonlyArray2<u32>, directed: bool) -> PyResult<CSRGraph> {
    let edges = edges.as_array();

    let num_nodes = match edges.iter().max() {
        Some(value) => *value + 1,
        _ => 0,
    };
    let num_edges = if directed {
        edges.len()
    } else {
        edges.len() * 2
    };

    let mut graph = CSRGraph::new(num_nodes as usize, num_edges);

    // To reduce memory pressure, reuse outs for both:
    //
    // - start(n): where to write the next edge of node n when constructing the graph, and
    // - edge_start(n)/edge_end(n): traditional CSR outs array--where the edges of node n begin and
    //     end.

    // First, count degrees
    //
    // outs[0] = degree(0)
    // outs[1] = degree(1)
    // outs[2] = degree(2)
    for src in edges.column(0) {
        graph.outs[*src as usize] += 1;
    }
    if !directed {
        for dst in edges.column(1) {
            graph.outs[*dst as usize] += 1;
        }
    }

    // Then, sum degrees to get starting indices
    //
    // outs[0] = 0
    // outs[1] = start(0) = 0
    // outs[2] = start(1) = degree(0)
    // outs[3] = start(2) = degree(0) + degree(1)
    let mut prev_degree = graph.outs[0];
    let mut sum_degree = 0;
    graph.outs[0] = 0;

    for idx in 1..graph.outs.len() {
        let degree_n = graph.outs[idx];
        graph.outs[idx] = sum_degree;
        sum_degree += prev_degree;
        prev_degree = degree_n;
    }

    // Now, after adding edges and incrementing start(n), we get
    //
    // outs[0] = edge_start(0)
    // outs[1] = edge_end(0)/edge_start(1)
    // outs[2] = edge_end(1)/edge_start(2)
    let mut add_edge = |src: NodeT, dst: NodeT| {
        let idx = graph.outs[src as usize + 1];

        graph.outs[src as usize + 1] += 1;

        graph.neighbors[idx as usize] = dst;
    };

    for row in edges.rows() {
        add_edge(row[0], row[1]);
        if !directed {
            add_edge(row[1], row[0]);
        }
    }

    for src in 0..graph.num_nodes() {
        graph.out_neighbors_slice_mut(src).sort();
    }

    Ok(graph)
}

fn random_neighbor(graph: &CSRGraph, src: NodeT, random: &mut FastRandom) -> Option<NodeT> {
    let neighbors = graph.out_neighbors_slice(src);
    let num_neighbors = neighbors.len();

    if num_neighbors == 0 {
        return None;
    }

    let next_neighbor = random.next_i32(num_neighbors as i32);

    Some(neighbors[next_neighbor as usize])
}

/// Write random walk starting at src into the given Vec.
///
/// random_walk will resize the given Vec to the length of the walk. The length of the walk will be
/// no greater than walk_length but may be shorter. Non-zero walks always begin with the start
/// node.
pub fn random_walk(
    graph: &CSRGraph,
    start_node: NodeT,
    max_walk_length: usize,
    p: f32,
    q: f32,
    random: &mut FastRandom,
    walk: &mut Vec<NodeT>,
) {
    let max_prob = 1f32.max(1. / q).max(1. / p);
    let prob_0 = 1. / p / max_prob;
    let prob_1 = 1. / max_prob;
    let prob_2 = 1. / q / max_prob;

    if max_walk_length == 0 {
        walk.truncate(0);
        return;
    } else if max_walk_length == 1 {
        walk.resize(1, 0);
        walk[0] = start_node;
        return;
    }

    let r = random_neighbor(graph, start_node, random);
    match r {
        Some(neighbor) => {
            walk.resize(max_walk_length, 0);
            walk[0] = start_node;
            walk[1] = neighbor;
        }
        None => {
            walk.resize(1, 0);
            walk[0] = start_node;
            return;
        }
    }

    for walk_idx in 2..max_walk_length {
        let r = random_neighbor(graph, walk[walk_idx - 1], random);
        match r {
            Some(neighbor) => {
                walk[walk_idx] = neighbor;
            }
            None => {
                walk.resize(walk_idx, 0);
                return;
            }
        }
        if p == q && q == 1. {
            continue;
        }

        loop {
            let sample = random.next_f32();

            if walk[walk_idx] == walk[walk_idx - 2] {
                if sample < prob_0 {
                    break;
                }
            } else if graph.has_edge(walk[walk_idx - 2], walk[walk_idx]) {
                if sample < prob_1 {
                    break;
                }
            } else if sample < prob_2 {
                break;
            }

            walk[walk_idx] = random_neighbor(graph, walk[walk_idx - 1], random).unwrap_or(0);
        }
    }
}
