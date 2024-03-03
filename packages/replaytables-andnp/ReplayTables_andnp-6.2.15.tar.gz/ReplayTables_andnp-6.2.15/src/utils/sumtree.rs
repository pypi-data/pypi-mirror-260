use numpy::{ToPyArray, PyArray1, PyReadonlyArray1};
use ndarray::{s, Array1, Array2, Axis};
use std::iter;
use std::cmp::*;
use pyo3::{prelude::*, types::{PyBytes, PyTuple}};
use bincode::{deserialize, serialize};
use serde::{Deserialize, Serialize};

#[pyclass(module = "rust")]
#[derive(Serialize, Deserialize)]

pub struct SumTree {
    #[pyo3(get)]
    size: u32,
    #[pyo3(get)]
    dims: u32,
    total_size: u32,
    raw: Vec<Array2<f64>>,
}

#[pymethods]
impl SumTree {
    #[new]
    #[pyo3(signature = (*args))]
    fn new(args: &PyTuple) -> Self {
        match args.len() {
            0 => SumTree {
                size: 0,
                dims: 0,
                total_size: 0,
                raw: vec![],
            },

            2 => {
                let size = args
                    .get_item(0).unwrap()
                    .extract::<u32>().unwrap();

                let dims = args
                    .get_item(1).unwrap()
                    .extract::<u32>().unwrap();

                let total_size = u32::next_power_of_two(size);
                let n_layers = u32::ilog2(total_size) + 1;

                let dummy = Array2::<f64>::zeros((1, 1));
                let mut layers = vec![dummy; n_layers as usize];

                for i in (0..n_layers).rev() {
                    let r = n_layers - i - 1;
                    let layer = Array2::<f64>::zeros((dims as usize, usize::pow(2, i)));
                    layers[r as usize] = layer;
                }

                SumTree {
                    size,
                    dims,
                    total_size,
                    raw: layers,
                }
            },

            _ => unreachable!(),
        }
    }

    pub fn update(
        &mut self,
        dim: u32,
        idxs: PyReadonlyArray1<i64>,
        values: PyReadonlyArray1<f64>,
    ) {
        for (idx, v) in iter::zip(idxs.as_array(), values.as_array()) {
            self.update_single(dim, *idx, *v);
        }
    }

    pub fn update_single(
        &mut self,
        dim: u32,
        idx: i64,
        value: f64,
    ) {
        if idx >= self.size as i64 {
            panic!("Tried to update index outside of tree: <{idx}>");
        }

        let mut sub_idx = idx as usize;
        let old = self.raw[0][[dim as usize, sub_idx]];

        let len = self.raw.len();
        for i in 0..len {
            self.raw[i][[dim as usize, sub_idx]] += value - old;
            sub_idx = sub_idx / 2;
        }
    }

    pub fn get_value(&mut self, dim: u32, idx: i64) -> f64 {
        self.raw[0][[dim as usize, idx as usize]]
    }

    pub fn get_values<'py>(
        &mut self,
        dim: u32,
        idxs: PyReadonlyArray1<i64>,
        py: Python<'py>,
    ) -> &'py PyArray1<f64> {
        let idxs = idxs.as_array().map(|a| { *a as usize });
        let arr = self.raw[0]
            .slice(s![dim as usize, ..])
            .select(Axis(0), &idxs.to_vec());

            arr.to_pyarray(py)
    }

    pub fn dim_total(&mut self, dim: u32) -> f64 {
        *self.raw
            .last()
            .expect("")
            .get((dim as usize, 0))
            .expect("")
    }

    pub fn all_totals<'py>(
        &mut self,
        py: Python<'py>,
    ) -> &'py PyArray1<f64> {
        let arr = self.raw
            .last()
            .expect("")
            .slice(s![.., 0]);

        arr.to_pyarray(py)
    }

    pub fn total(
        &mut self,
        w: PyReadonlyArray1<f64>,
    ) -> f64 {
        let x = self.raw
            .last()
            .expect("")
            .slice(s![.., 0]);

        w.as_array().dot(&x)
    }

    pub fn effective_weights<'py>(
        &mut self,
        py: Python<'py>,
    ) -> &'py PyArray1<f64> {
        let arr = self.raw
            .last()
            .expect("")
            .slice(s![.., 0]);

        let arr: Array1<f64> = arr.map(safe_invert);
        arr.to_pyarray(py)
    }

    pub fn query<'py>(
        &mut self,
        v: PyReadonlyArray1<f64>,
        w: PyReadonlyArray1<f64>,
        py: Python<'py>,
    ) -> &'py PyArray1<i64> {
        let n = v.len();
        let n_layers = self.raw.len();

        let w = w.as_array();
        let v = v.as_array();
        let mut totals = Array1::<f64>::zeros(n);
        let mut idxs = Array1::<i64>::zeros(n);

        for i in (0..n_layers).rev() {
            let layer = &self.raw[i];

            for j in 0..n {
                idxs[j] = idxs[j] * 2;
                let part = layer.slice(s![.., idxs[j] as usize]);
                let left = w.dot(&part);

                let m = left < (v[j] - totals[j]);
                totals[j] += if m { left } else { 0. };
                idxs[j] += if m { 1 } else { 0 };
            }
        }

        idxs = idxs.map(|i| { min(*i, (self.size - 1) as i64) });
        idxs.to_pyarray(py)
    }

    // enable pickling this data type
    pub fn __setstate__(&mut self, state: &PyBytes) -> PyResult<()> {
        *self = deserialize(state.as_bytes()).unwrap();
        Ok(())
    }
    pub fn __getstate__<'py>(&self, py: Python<'py>) -> PyResult<&'py PyBytes> {
        Ok(PyBytes::new(py, &serialize(&self).unwrap()))
    }
}

fn safe_invert(a: &f64) -> f64 {
    if *a == 0. {
        0.
    } else {
        1. / *a
    }
}
