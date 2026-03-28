use pyo3::prelude::*;
use pyo3::types::PyDict;
use rand::{Rng, SeedableRng, rngs::StdRng};
use std::collections::HashMap;

/// A high-performance state container for seed simulation.
#[pyclass]
pub struct Sprout {
    buds: HashMap<u32, u32>,
    rng: StdRng,
    #[pyo3(get)]
    pub seed: u64,
}

#[pymethods]
impl Sprout {
    #[new]
    fn new(seed: u64) -> Self {
        Self {
            buds: HashMap::with_capacity(10),
            rng: StdRng::seed_from_u64(seed),
            seed,
        }
    }

    /// Resets the sprout state to allow memory reuse in tight loops.
    fn reset(&mut self, new_seed: u64) {
        self.buds.clear();
        self.seed = new_seed;
        self.rng = StdRng::seed_from_u64(new_seed);
    }

    /// Registers a count for a specific bud ID.
    #[pyo3(signature = (bud_id, count=None))]
    fn add_bud(&mut self, bud_id: u32, count: Option<u32>) {
        let count = count.unwrap_or(1);
        if count > 0 {
            *self.buds.entry(bud_id).or_insert(0) += count;
        }
    }

    /// Retrieves the current count for a bud ID without Python overhead.
    fn get_bud_count(&self, bud_id: u32) -> u32 {
        *self.buds.get(&bud_id).unwrap_or(&0)
    }

    /// Generates a random integer within an inclusive range using the internal PRNG.
    fn growth(&mut self, a: i32, b: i32) -> i32 {
        self.rng.gen_range(a..=b)
    }

    /// Exports the internal bud mapping to a Python dictionary.
    fn to_dict<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyDict>> {
        let dict = PyDict::new(py);
        for (&k, &v) in &self.buds {
            dict.set_item(k, v)?;
        }
        Ok(dict)
    }
}

/// The execution engine for batch-processing and filtering sprouts.
#[pyclass(subclass)]
pub struct PlanterLab {}

#[pymethods]
impl PlanterLab {
    #[new]
    fn new() -> Self { Self {} }

    /// Orchestrates a search loop across a range of seeds.
    #[pyo3(signature = (fire=None, minimum=0, maximum=100_000))]
    fn find_seeds<'py>(
        slf: Bound<'py, Self>,
        fire: Option<Bound<'py, PyAny>>,
        minimum: u64,
        maximum: u64,
    ) -> PyResult<Vec<(u64, PyObject)>> {
        let py = slf.py();
        let mut results = Vec::with_capacity(100);
        let mut sprout = Sprout::new(0);

        for i in minimum..maximum {
            sprout.reset(i);
            
            let bound_sprout = Bound::new(py, Sprout {
                buds: sprout.buds.clone(),
                rng: sprout.rng.clone(),
                seed: sprout.seed,
            })?;

            slf.call_method1("plant", (&bound_sprout,))?;

            {
                let updated = bound_sprout.borrow();
                sprout.buds = updated.buds.clone();
            }

            let should_purge = if let Some(ref fire_obj) = fire {
                fire_obj.call_method1("purge", (bound_sprout,))?.extract::<bool>()?
            } else {
                false
            };

            if !should_purge {
                results.push((sprout.seed, sprout.to_dict(py)?.into_any().unbind()));
            }
        }
        Ok(results)
    }

    /// Interface method for defining bud growth logic in Python.
    fn plant(&self, _sprout: Bound<'_, Sprout>) -> PyResult<()> {
        Ok(())
    }
}

#[pymodule]
fn seedler_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Sprout>()?;
    m.add_class::<PlanterLab>()?;
    Ok(())
}