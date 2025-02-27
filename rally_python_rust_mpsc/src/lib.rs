use std::sync::{mpsc, Arc};
use std::sync::mpsc::{Sender};
use std::thread;
use pyo3::prelude::*;

#[pyfunction]
fn ready(callback: PyObject) -> TickSender {
    let wrapped = Arc::new(callback);
    let (tx, rx) = mpsc::channel::<i32>();
    thread::spawn(move || {
        for num in rx {
            println!("RUST 수신: {}: {:?}", num, thread::current().id());
            let func = wrapped.clone();
            thread::spawn(move || {
                println!("RUST 작업: {}, {:?}", num, thread::current().id());
                Python::with_gil(|py| {
                    let args = ("OK",);
                    func.call1(py, args).unwrap();
                });
            });
            println!("RUST WORK DONE");
        }
        eprintln!("RUST: Channel Finished");
    });
    TickSender(tx)
}

/// A Python module implemented in Rust.
#[pymodule]
fn rally_python_rust_mpsc(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(ready, m)?)?;
    Ok(())
}

/// Sender Wrapper
#[pyclass]
struct TickSender (Sender<i32>);

#[pymethods]
impl TickSender {
    pub fn send(&self, num: i32) -> PyResult<i32> {
        self.0.send(num).unwrap();
        Ok(0)
    }
}
