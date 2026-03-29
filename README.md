# Seedler

Seedler is a high-performance Python package powered by Rust, designed for large-scale Monte Carlo simulations and RNG seed discovery. By leveraging Rust's speed and safety alongside Python's flexibility, Seedler allows you to simulate millions of scenarios, filter results with complex logic, and perfectly recreate specific outcomes using deterministic seeding.


## Key Features
* **Fast Core**: Simulation loops and RNG generation are handled in Rust.
* **Deterministic Re-simulation**: Every result is tied to a u64 seed, allowing 100% reproducible results.
* **Flexible Callbacks**: Use Python classes to define your "Planter" (simulation logic) and "Fire" (filtering logic).
* **Memory Efficient**: Designed to handle millions of iterations without ballooning memory usage.

## Installation

### Pip
```bash
pip install git+https://github.com/byuirpytooling/seedler.git@main
```

### UV
```bash
uv pip install git+https://github.com/byuirpytooling/seedler.git@main
```

### Development
From Source. Seedler requires the Rust toolchain and maturin to build the native extension.

```bash
git clone git+https://github.com/byuirpytooling/seedler.git@main
cd seedler-repo

uv venv --python 3.14
source .venv/bin/activate

uv pip install -e .
uv run maturin develop
```

## Quick Start
Seedler uses *Garden* and *Planting* metaphors for simulations:

1. **Sprout**: The container for a single simulation run (holds the RNG and results).
2. **Planter**: Defines the logic of what happens during the simulation.
3. **Fire**: Defines the conditions that "purge" (filter out) a simulation.

### Simple 3-Card Monte Example

Find which seeds result in a "Win" (selecting the passing card) out of 100 simulations.

```python
from seedler import Planter, Sprout, Fire

# Flags
WIN = 0
LOSE = 1

# 1. Define your Simulation Logic
class CardMontePlanter(Planter):
    def plant(self, sprout: Sprout):
        # 0 is Win, 1 & 2 are Lose
        cards = [WIN, LOSE, LOSE]
        # Use Rust-backed RNG via sprout.growth(min, max)
        outcome = cards[sprout.growth(0, 2)]
        sprout.add_bud(outcome)

# 2. Define your Filtering Logic
class PurgeLosses(Fire):
    def purge(self, sprout: Sprout):
        # If we didn't get a 'WIN', burn the seed
        return sprout.get_bud_count(WIN) == 0

# 3. Run the Lab
lab = CardMontePlanter()
winning_seeds = lab.find_seeds(
    fire=PurgeLosses(), 
    minimum=0, 
    maximum=100
)

print(f"Found {len(winning_seeds)} winning seeds.")
```

### Re-Simulating Single Seeds

One of Seedler's strengths is the ability to recreate a complex simulation state instantly using only its seed.

```Python
# Assuming you have a seed from a previous run
seed = [EXAMPLE SEED]

sprout = Sprout(seed)
lab.plant(sprout)

print(f"Results for seed {seed}: {sprout.to_dict()}")
```

## Data Analysis with Pandas

Seedler integrates seamlessly with Pandas for post-simulation analysis. The get_data() method returns a structured format that can be converted into a DataFrame instantly.

```Python
import pandas as pd
from seedler import PlanterLab

lab = MyCustomPlanter()
results = lab.find_seeds(minimum=0, maximum=1000)

# Convert Planter results to a DataFrame
# get_data() returns List[Tuple[int, Dict]]
df = pd.DataFrame([
    {"seed": seed, **data} 
    for seed, data in results
])

# Perform standard analysis
print(df.describe())
print(df['my_stat'].mean())
```

## Benchmarking

Seedler is optimized for "Seed Hunting"—searching for specific RNG outcomes across massive ranges. Because the loop and RNG state reside in Rust, Seedler significantly outperforms pure Python implementations by minimizing the overhead of the Python interpreter for the core simulation logic.

| Iterations | Pure Python (s) | Seedler (s) | Speedup |
| ---: | ---: | ---: | ---: |
| 100,000 | *0.58* | *0.06* | 9.00x |
| 1,000,000 | *5.68* | *0.67* | 8.51x |
| 5,000,000 | *28.51* | *3.35* | 8.50x |
| 10,000,000 | *58.07* | *7.20* | 8.07x |

> **Note:** Benchmarks performed on Apple M3 Pro, 8GB RAM. Actual performance gains scale with the number of iterations and the efficiency of your Python-side `plant` and `purge` callbacks.


## Contributing

Contributions are welcome! Please ensure that any Rust changes include updated tests and satisfy `cargo fmt`.

- Fork the Project
- Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
- Commit your Changes (`git commit -m 'Add AmazingFeature'`)
- Push to the Branch (`git push origin feature/AmazingFeature`)
- Open a Pull Request

## License

Distributed under the MIT License. See LICENSE for more information.

Authors: 

- **Dallin Wolfer** - wol23003@byui.edu
- **Alyssa Cox** -

Project Link: https://github.com/byuirpytooling/seedler