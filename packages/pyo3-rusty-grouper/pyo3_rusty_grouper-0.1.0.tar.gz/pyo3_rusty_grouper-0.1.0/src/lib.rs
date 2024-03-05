mod grouper;

use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn group_keywords(file_path: &str) -> PyResult<Vec<Vec<String>>> {
    Ok(grouper::group_keywords(file_path))
}

/// A Python module implemented in Rust.
#[pymodule]
fn pyo3_rusty_grouper(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(group_keywords, m)?)?;
    Ok(())
}
