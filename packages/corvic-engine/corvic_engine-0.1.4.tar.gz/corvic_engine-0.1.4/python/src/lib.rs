#![feature(unsafe_cell_from_mut)]
use graph::CSRGraph;
use node2vec::Node2VecParams;
use pyo3::prelude::*;

mod datarace;
mod fastfn;
mod graph;
mod node2vec;
mod random;

/// A Python module implemented in Rust.
#[pymodule]
#[pyo3(name = "_native")]
fn engine(_py: Python, m: &PyModule) -> PyResult<()> {
    fastfn::init_sigmoid_table();
    m.add_function(wrap_pyfunction!(node2vec::train_node2vec_epoch, m)?)?;
    m.add_function(wrap_pyfunction!(graph::csr_from_edges, m)?)?;
    m.add_class::<CSRGraph>()?;
    m.add_class::<Node2VecParams>()?;
    Ok(())
}
