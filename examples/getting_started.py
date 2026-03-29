## QUICK START
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 

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

# >>> Found 32 winning seeds.
print(f"Found {len(winning_seeds)} winning seeds.")




## Re-Simulating Seeds
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 

seed = winning_seeds[0][0]

sprout = Sprout(seed)
lab.plant(sprout)

# >>> Results for seed 2: {0: 1}
# Flag 0: WIN, count 1
print(f"Results for seed {seed}: {sprout.to_dict()}")




## Data Analysis
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 

import pandas as pd

df = pd.DataFrame([
    {"seed": seed, **data} 
    for seed, data in winning_seeds
])

print(df.describe())
print(f"Wins: {df[WIN].sum()}")