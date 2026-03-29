# Imports
from seedler import Planter, Sprout, Fire, Nursery
import numpy as np
import pandas as pd

# Sim settings
test_range = 100
test_runs = 10_000_000

# Lab
class MyLab(Planter):
    def plant(self, sprout: Sprout):
        sprout.add_bud(sprout.growth(0,test_range - 1))


lab = MyLab()
planter = lab.find_seeds(maximum=test_runs)
total_counts = np.zeros(test_range, dtype=np.int64)

for _, data_dict in planter:
    if not data_dict:
        continue
    keys = np.fromiter(data_dict.keys(), dtype=np.int32)
    vals = np.fromiter(data_dict.values(), dtype=np.int32)
    total_counts[keys] += vals

df = pd.DataFrame({
    "Key": np.arange(test_range),
    "Count": total_counts
})

# results
exp_mean = (test_range - 1) / 2.0
exp_std = ((test_range**2 - 1) / 12) ** 0.5
exp_mean_error = exp_std / (df["Count"].sum() ** 0.5)

total_samples = int(df["Count"].sum())

actual_mean = (df["Key"] * df["Count"]).sum() / total_samples

weighted_variance = (df["Count"] * (df["Key"] - actual_mean)**2).sum() / total_samples
actual_std = weighted_variance ** 0.5

actual_mean_error = abs(actual_mean - exp_mean)

print(f"Total Samples Run:  {total_samples:,}")
print("-" * 40)
print(f"Expected Mean:      {exp_mean:>10.3f} | Actual Weighted Mean: {actual_mean:>10.3f}")
print(f"Expected STD:       {exp_std:>10.3f} | Actual Weighted STD:  {actual_std:>10.3f}")
print(f"Expected Error:     {exp_mean_error:>10.3f} | Actual Mean Error:    {actual_mean_error:>10.3f}")