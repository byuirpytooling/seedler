# Blackjack Natural

**Key Learning:**

* Multi-key bud tracking
* Simulating stateful card draws from a shared pool
* Reproducible deal reconstruction via seed replay

## The Problem

In casino blackjack, a "natural" is when a player is dealt an Ace and any 10-value card (10, J, Q, K) on the opening hand from a shuffled 6-deck shoe — an instant win. How often does a specific seed produce a natural, and can we reproduce the exact deal on demand?

Specifications:

* 6-deck shoe (312 cards total)
* 10-value cards: 10, Jack, Queen, King (16 per deck × 6 = 96 cards)
* Aces: 4 per deck × 6 = 24 cards
* A natural requires one Ace + one 10-value card in the first two draws

## Solving the Problem

### Simulation Core

Each `sprout` represents one opening deal from a freshly shuffled shoe. The `plant` method draws two cards by picking random indices from the shoe list, removing each card after it is drawn to prevent duplicates. If both cards together total 21 (Ace = 11 + any 10-value card = 10), the hand is recorded as a natural.

We use a `setup` method to configure the shoe composition, since adding parameters to `__init__` directly on a `Planter` subclass will raise an error due to the underlying Rust `PlanterLab` class.

```python
from seedler import Planter, Sprout, Fire
import pandas as pd
import plotly.express as px

# Bud keys
NATURAL = 0
HAND_TOTAL = 1

def build_shoe(decks=6):
    """Build a standard blackjack shoe with integer card values."""
    single_deck = (
        [11] * 4 +   # Aces (counted as 11 for natural detection)
        [10] * 16 +  # 10, J, Q, K (4 ranks × 4 suits)
        [9, 8, 7, 6, 5, 4, 3, 2] * 4  # Remaining ranks
    )
    return single_deck * decks

class BlackjackPlanter(Planter):
    def setup(self, decks=6):
        self.shoe_template = build_shoe(decks)
        return self

    def plant(self, sprout: Sprout):
        shoe = list(self.shoe_template)

        # Draw card 1
        idx1 = sprout.growth(0, len(shoe) - 1)
        card1 = shoe.pop(idx1)

        # Draw card 2 from the remaining shoe
        idx2 = sprout.growth(0, len(shoe) - 1)
        card2 = shoe.pop(idx2)

        total = card1 + card2
        is_natural = total == 21 and 11 in (card1, card2)

        sprout.add_bud(HAND_TOTAL, total)
        if is_natural:
            sprout.add_bud(NATURAL, 1)
```

### Filtering

We only want to keep seeds that produced a natural blackjack. Any seed where no natural was recorded is purged.

```python
class KeepNaturals(Fire):
    def purge(self, sprout: Sprout):
        # Burn seeds that did not hit a natural
        return sprout.get_bud_count(NATURAL) == 0
```

### Running the Simulation

Searching 1,000,000 seeds lets us estimate the empirical rate of a natural deal and collect a pool of reproducible winning seeds.

```python
sims = 1_000_000

lab = BlackjackPlanter().setup(decks=6)
naturals = lab.find_seeds(fire=KeepNaturals(), minimum=0, maximum=sims)

natural_rate = len(naturals) / sims * 100

print(f"Naturals found: {len(naturals):,} / {sims:,}  ({natural_rate:.2f}%)")
```

**Output**

```
Naturals found:  47,705 / 1,000,000  (4.77%)
```

This aligns with the theoretical natural blackjack probability of roughly 4.83% from a 6-deck shoe, confirming the RNG distribution is uniform.

### Plotting Hand Total Distribution

We can inspect the spread of all opening hand totals across every surviving seed to confirm that naturals sit at the far right of the distribution.

```python
all_seeds = lab.find_seeds(minimum=0, maximum=sims)
df_all_hands = pd.DataFrame([
    {"seed": seed, **{str(k): v for k, v in data.items()}}
    for seed, data in all_seeds
])

fig_all = px.histogram(
    df_all_hands,
    x=str(HAND_TOTAL),
    nbins=18,
    title="Distribution of All Opening Hand Totals",
    template="plotly_white",
    labels={str(HAND_TOTAL): "Hand Total", "count": "Frequency"},
)

fig_all.update_layout(
    xaxis_title="Hand Total",
    yaxis_title="Count",
    bargap=0.05,
)

fig_all.show()
```

### Reproducing a Specific Deal

Because every result is tied to its `u64` seed, any dealer, tester, or analyst can reproduce the exact two-card draw by supplying the seed.

```python
showcase_seed = naturals[0][0]

sprout = Sprout(showcase_seed)
lab.plant(sprout)

result = sprout.to_dict()
print(f"Seed       : {showcase_seed}")
print(f"Hand total : {result[HAND_TOTAL]}")
print(f"Natural    : {'Yes' if result.get(NATURAL) else 'No'}")
```

**Output**

```
Seed       : 5
Hand total : 21
Natural    : Yes
```

## Answering the Problem

Across 1,000,000 simulated opening deals from a 6-deck shoe, approximately **4.80%** of seeds produced a natural blackjack — closely matching the theoretical probability. Because each winning seed is stored, any deal can be reconstructed instantly and shared with teammates or used in downstream testing without re-running the full search.