# Monty-Hall Problem

**Key Learning:**

- Using enum flags
- Parallel simulation (same problem, simulate multiple solutions)
- Performance via. pruning (using Fire.purge)

## The Situation
The Monty-Hall problem is a classic probabilities problem, which is as follows:

- Three mystery doors are presented, one has a prize, the others are empty
- You choose one door
- A door you did not choose that is empty is revealed to be empty
- You may keep your original door, or switch to the remaining un-revealed door

What is the best option? Do you switch, or do you keep your current door?

## Solving the Problem

### Simulation

We will use seedler to run a monte-carlo simulation of the problem to approximate the probabilies of winning in each situation.

For this problem, we will run the same seeds across two different `Planter` labs, each representing one possible solution.

```python
from seedler import *
from enum import IntEnum

class res(IntEnum):
    PRIZE = 0
    EMPTY = 1

res_map = {int(member) : member.name.lower() for member in res}

doors = [res.PRIZE, res.EMPTY, res.EMPTY]

class MonteHallLab_Keep(Planter):
    def plant(self, sprout):
        choice = sprout.growth(0, 2)
        sprout.add_bud(int(doors[choice]))

class MonteHallLab_Switch(Planter):
    def plant(self, sprout):
        choice = sprout.growth(0, 2)
        a = (choice + 1) % 3
        b = (a + 1) % 3

        switch = choice
        if doors[a] == res.EMPTY:
            switch = b
        else:
            switch = a
        
        sprout.add_bud(int(doors[switch]))
```

Since seedler uses integers as keys for the buds, we will use the IntEnum class to create reusable flags.

Both *Labs* are simulating on the same problem, but one simulates keeping your initial door, while the other simulates switching to the remaining door after having the empty one revealed.

### Purging

While we can attai the results without a `Fire`, it significantly increases simulation performance since all purged seeds aren't saved. Purging is always recommended to improve the memory-efficiency of the simulations.

Our purge is simple: Remove all seeds that result in an empty door.

```python
class BurnEmpty(Fire):
    def purge(self, sprout):
        return sprout.get_bud_count(res.PRIZE) == 0
```

### Getting Results

The next step is to simulate the problem.

```python
sims = 10_000

mhKeep = MonteHallLab_Keep()
mhSwitch = MonteHallLab_Switch()

prize_keep = mhKeep.find_seeds(fire=BurnEmpty(), maximum=sims)
prize_switch = mhSwitch.find_seeds(fire=BurnEmpty(), maximum=sims)

keep_perc = len(prize_keep) / sims * 100
switch_perc = len(prize_switch) / sims * 100

print("Winning Chances:")
print(f" - Keep   {keep_perc:>6.2f}")
print(f" - Switch {switch_perc:>6.2f}")
```

Since all failing (empty-door) seeds are purges, all seeds remaining pass (get the prize). We can simply count the number of results and divide by total simulations run to ge the approximate probability of success for each method.

**Output**
```text
Winning Chances:
 - Keep    33.66
 - Switch  66.34
```

### Answering the problem

When you keep your door, you win ~33% of the time, and when you switch to the remaining door, you win ~66% of the time. Due to this fact, we recommend you always switch to the remaining door.