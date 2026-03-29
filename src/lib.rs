use pyo3::prelude::*;
use pyo3::types::PyDict;
use rand::{rngs::StdRng, Rng, SeedableRng};
use std::collections::HashMap;

/// A high-performance state container for seed simulation.
///
/// The Sprout holds the internal RNG state and a collection of 'buds' (event counts).
/// It is designed to be passed between the Planter (logic) and Fire (filter).
#[pyclass]
pub struct Sprout {
    buds: HashMap<u32, u32>,
    rng: StdRng,
    /// The u64 seed used to initialize this specific sprout's RNG.
    #[pyo3(get)]
    pub seed: u64,
}

#[pymethods]
impl Sprout {
    #[new]
    /// Initializes a new Sprout.
    ///
    /// Args:
    ///     seed (int): The initial u64 seed for deterministic randomness.
    fn new(seed: u64) -> Self {
        Self {
            buds: HashMap::with_capacity(10),
            rng: StdRng::seed_from_u64(seed),
            seed,
        }
    }

    /// Resets the sprout state to allow memory reuse in tight loops.
    ///
    /// Args:
    ///     new_seed (int): The new seed to re-initialize the PRNG.
    fn reset(&mut self, new_seed: u64) {
        self.buds.clear();
        self.seed = new_seed;
        self.rng = StdRng::seed_from_u64(new_seed);
    }

    /// Registers a count for a specific bud ID.
    ///
    /// Args:
    ///     bud_id (int): A unique identifier for the event/item being tracked.
    ///     count (int, optional): The amount to increment by. Defaults to 1.
    #[pyo3(signature = (bud_id, count=None))]
    fn add_bud(&mut self, bud_id: u32, count: Option<u32>) {
        let count = count.unwrap_or(1);
        if count > 0 {
            *self.buds.entry(bud_id).or_insert(0) += count;
        }
    }

    /// Retrieves the current count for a bud ID without Python overhead.
    ///
    /// Args:
    ///     bud_id (int): The ID to look up.
    ///
    /// Returns:
    ///     int: The current count, or 0 if the ID has not been added.
    fn get_bud_count(&self, bud_id: u32) -> u32 {
        *self.buds.get(&bud_id).unwrap_or(&0)
    }

    /// Generates a random integer within an inclusive range using the internal PRNG.
    ///
    /// Args:
    ///     a (int): Inclusive lower bound.
    ///     b (int): Inclusive upper bound.
    ///
    /// Returns:
    ///     int: A pseudo-random integer.
    fn growth(&mut self, a: i32, b: i32) -> i32 {
        self.rng.gen_range(a..=b)
    }

    /// Exports the internal bud mapping to a Python dictionary.
    ///
    /// Returns:
    ///     dict: A dictionary mapping bud_ids to their respective counts.
    fn to_dict<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyDict>> {
        let dict = PyDict::new(py);
        for (&k, &v) in &self.buds {
            dict.set_item(k, v)?;
        }
        Ok(dict)
    }
}

/// The execution engine for batch-processing and filtering sprouts.
///
/// PlanterLab handles the heavy lifting of iterating through seed ranges
/// in compiled code while calling back to Python for custom logic.
#[pyclass(subclass)]
pub struct PlanterLab {}

#[pymethods]
impl PlanterLab {
    #[new]
    fn new() -> Self {
        Self {}
    }

    /// Orchestrates a search loop across a range of seeds.
    ///
    /// This method iterates from minimum to maximum, creating a Sprout for each
    /// seed, executing 'plant', and checking the 'fire' filter.
    ///
    /// Args:
    ///     fire (Fire, optional): A filter object with a 'purge' method.
    ///     minimum (int): The starting seed (inclusive).
    ///     maximum (int): The ending seed (exclusive).
    ///
    /// Returns:
    ///     list[tuple[int, dict]]: A list of tuples containing (seed, results_dict).
    #[pyo3(signature = (fire=None, minimum=0, maximum=100_000))]
    fn find_seeds<'py>(
        slf: Bound<'py, Self>,
        fire: Option<Bound<'py, PyAny>>,
        minimum: u64,
        maximum: u64,
    ) -> PyResult<Vec<(u64, PyObject)>> {
        // ... (Logic remains unchanged) ...
        let py = slf.py();
        let mut results = Vec::with_capacity(100);
        let mut sprout = Sprout::new(0);

        for i in minimum..maximum {
            sprout.reset(i);

            let bound_sprout = Bound::new(
                py,
                Sprout {
                    buds: sprout.buds.clone(),
                    rng: sprout.rng.clone(),
                    seed: sprout.seed,
                },
            )?;

            slf.call_method1("plant", (&bound_sprout,))?;

            {
                let updated = bound_sprout.borrow();
                sprout.buds = updated.buds.clone();
            }

            let should_purge = if let Some(ref fire_obj) = fire {
                fire_obj
                    .call_method1("purge", (bound_sprout,))?
                    .extract::<bool>()?
            } else {
                false
            };

            if !should_purge {
                results.push((sprout.seed, sprout.to_dict(py)?.into_any().unbind()));
            }
        }
        Ok(results)
    }

    /// Interface method for defining bud growth logic. 
    /// 
    /// Users should subclass PlanterLab and override this method in Python.
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