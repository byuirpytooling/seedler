# Perfect Run Seed Hunter

**Key Learning:**

* Stateful multi-step simulations with carry-over state
* Hunting rare compound outcomes across millions of seeds
* Using seeds as shareable, reproducible tokens

## The Problem

In a procedurally generated obstacle course game, an agent must clear five consecutive obstacles. Each obstacle has a base 60% clear chance, but consecutive successes raise a fatigue counter that makes each following obstacle harder. How rare is a "perfect run" (clearing all five), and can we find seeds that guarantee one on demand?

Specifications:

* 5 obstacles per run
* Base clear threshold: 6 out of 10
* Fatigue: +1 per consecutive clear, −1 on fail (minimum 0), applied to the threshold
* A perfect run requires all 5 obstacles cleared

## Solving the Problem

### Simulation Core

Each `sprout` represents one full attempt at the course. The `plant` method steps through each obstacle, rolls an RNG value, and compares it against the current threshold after applying fatigue. State (fatigue, clear/fail counts) carries forward from one obstacle to the next within the same sprout.

We use a `setup` method to configure the number of obstacles and base difficulty, since adding parameters to `__init__` directly on a `Planter` subclass will raise an error due to the underlying Rust `PlanterLab` class.

```python
from seedler import Planter, Sprout, Fire
import pandas as pd
import plotly.express as px

# Bud keys
CLEARS = 0
FAILS  = 1

class ObstaclePlanter(Planter):
    def setup(self, obstacles=5, base_threshold=6):
        self.obstacles = obstacles
        self.base_threshold = base_threshold
        return self

    def plant(self, sprout: Sprout):
        fatigue = 0
        clears  = 0
        fails   = 0

        for _ in range(self.obstacles):
            threshold = max(1, self.base_threshold - fatigue)
            roll = sprout.growth(1, 10)

            if roll <= threshold:
                clears  += 1
                fatigue += 1          # harder after each clear
            else:
                fails   += 1
                fatigue  = max(0, fatigue - 1)   # partial recovery on fail

        sprout.add_bud(CLEARS, clears)
        sprout.add_bud(FAILS,  fails)

    def plant_verbose(self, sprout: Sprout):
        """Per-obstacle breakdown for replay visualization."""
        fatigue = 0

        for step in range(self.obstacles):
            threshold = max(1, self.base_threshold - fatigue)
            roll = sprout.growth(1, 10)

            cleared = 1 if roll <= threshold else 0
            fatigue = (fatigue + 1) if cleared else max(0, fatigue - 1)
            sprout.add_bud(step, cleared)
```

### Filtering

We only keep seeds where the agent cleared every obstacle. Any seed with fewer than `self.obstacles` clears is purged.

```python
class RequirePerfectRun(Fire):
    def __init__(self, obstacles=5):
        self.obstacles = obstacles

    def purge(self, sprout: Sprout):
        # Burn any seed that dropped at least one obstacle
        return sprout.get_bud_count(CLEARS) < self.obstacles
```

### Running the Simulation

Searching 5,000,000 seeds gives a statistically stable estimate of how often a perfect run occurs under rising fatigue pressure.

```python
sims = 5_000_000

lab = ObstaclePlanter().setup(obstacles=5, base_threshold=6)
perfect_runs = lab.find_seeds(
    fire=RequirePerfectRun(obstacles=5),
    minimum=0,
    maximum=sims
)

perfect_rate = len(perfect_runs) / sims * 100

print(f"Perfect runs: {len(perfect_runs):,} / {sims:,}  ({perfect_rate:.3f}%)")
```

**Output**

```
Perfect runs: 36,010 / 5,000,000  (0.720%)
```

While a single obstacle has a 60% clear chance, the compounding fatigue penalty means only ~0.72% of all starting seeds produce a clean sweep — making perfect-run seeds genuinely rare.

### Plotting Clear Sequences

Re-simulating a subset of perfect-run seeds with `plant_verbose` lets us visualize the per-obstacle outcome for each run, confirming every step was cleared.

```python
if len(perfect_runs) == 0:
    quit()

target_seeds = [r[0] for r in perfect_runs[:50]]
all_paths = []

for seed_id in target_seeds:
    sprout = Sprout(seed_id)
    lab.plant_verbose(sprout)

    temp_df = pd.DataFrame(
        sprout.to_dict().items(),
        columns=["obstacle", "cleared"]
    )
    temp_df["seed"] = str(seed_id)
    all_paths.append(temp_df)

df_master = (
    pd.concat(all_paths)
    .sort_values(by=["seed", "obstacle"])
    .reset_index(drop=True)
)
```


```python
fig = px.line(
    df_master,
    x="obstacle",
    y="cleared",
    color="seed",
    title=f"Per-Obstacle Outcomes for {len(target_seeds)} Perfect-Run Seeds",
    template="plotly_white",
    render_mode="webgl",
)

fig.update_traces(
    line=dict(width=1),
    opacity=0.4,
)

fig.update_layout(
    showlegend=False,
    xaxis_title="Obstacle Index",
    yaxis_title="Cleared (1 = Yes, 0 = No)",
    yaxis=dict(tickvals=[0, 1]),
    hovermode="closest",
)

fig.show()
```

### Sharing a Seed as a Reproducible Token

Because every result is tied to its `u64` seed, a developer, QA tester, or content creator can share a single integer to guarantee another person sees the exact same run.

```python
showcase_seed = perfect_runs[0][0]

sprout = Sprout(showcase_seed)
lab.plant(sprout)

result = {CLEARS: 0, FAILS: 0}
result = sprout.to_dict()
print(f"Seed   : {showcase_seed}")
print(f"Clears : {result[CLEARS]}")
print(f"Fails  : {result[FAILS]}")
print(f"→ Share seed {showcase_seed} to replay this perfect run exactly.")
```

**Output**

```
Seed   : 26
Clears : 5
Fails  : 0
→ Share seed 26 to replay this perfect run exactly.
```

## Answering the Problem

Under a fatigue-adjusted difficulty model, only **~0.72%** of RNG seeds produce a perfect five-obstacle clear. Seedler locates all of them across 5,000,000 simulations in seconds. Each winning seed acts as a compact, shareable token — ideal for game QA, speedrun verification, or pre-recorded demo sequences where a guaranteed outcome is required.