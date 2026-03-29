import time
import pandas as pd
from seedler import Planter, Sprout, Fire

# --- Configuration ---
ITERATIONS = [100_000, 1_000_000, 5_000_000, 10_000_000]
PASS = 0
FAIL = 1

# --- Seedler Implementation ---
class MontePlanter(Planter):
    def plant(self, sprout: Sprout):
        # Simulate a 1/3 chance of success
        res = PASS if sprout.growth(0, 2) == 0 else FAIL
        sprout.add_bud(res)

class PurgeFail(Fire):
    def purge(self, sprout: Sprout):
        return sprout.get_bud_count(FAIL) >= 1

# --- Pure Python Implementation ---
import random

def run_pure_python(count):
    results = []
    for i in range(count):
        random.seed(i)
        # Simulate the same 1/3 logic
        card = PASS if random.randint(0, 2) == 0 else FAIL
        if card == PASS:
            results.append((i, {PASS: 1}))
    return results

# --- Execution ---
def run_benchmarks():
    data = []
    print(f"{'Iterations':<15} | {'Python (s)':<12} | {'Seedler (s)':<12} | {'Speedup'}")
    print("-" * 60)

    for count in ITERATIONS:
        # Benchmark Pure Python
        start_py = time.perf_counter()
        run_pure_python(count)
        end_py = time.perf_counter()
        py_time = end_py - start_py

        # Benchmark Seedler
        lab = MontePlanter()
        fire = PurgeFail()
        
        start_rust = time.perf_counter()
        lab.find_seeds(fire=fire, minimum=0, maximum=count)
        end_rust = time.perf_counter()
        rust_time = end_rust - start_rust

        speedup = py_time / rust_time
        data.append({
            "Iterations": count,
            "Python (s)": round(py_time, 4),
            "Seedler (s)": round(rust_time, 4),
            "Speedup": round(speedup, 2)
        })

        print(f"{count:<15} | {py_time:<12.4f} | {rust_time:<12.4f} | {speedup:.2f}x")

    return pd.DataFrame(data)

if __name__ == "__main__":
    print("🚀 Starting Seedler vs Pure Python Benchmark...\n")
    df = run_benchmarks()
    print("\n✅ Benchmark Complete.")