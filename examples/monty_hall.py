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

class BurnEmpty(Fire):
    def purge(self, sprout):
        return sprout.get_bud_count(res.PRIZE) == 0

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