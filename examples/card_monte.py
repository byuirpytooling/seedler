from seedler import Planter, Sprout, Fire

sims = 100

PASS = 0
FAIL = 1

class CardMontePlanter(Planter):
    def plant(self, sprout: Sprout):
        cards = [PASS, FAIL, FAIL]
        card = cards[sprout.growth(0, 2)]
        sprout.add_bud(card)

class PurgeFail(Fire):
    def purge(self, sprout: Sprout):
        return sprout.get_bud_count(FAIL) >= 1

class PurgePass(Fire):
    def purge(self, sprout: Sprout):
        return sprout.get_bud_count(PASS) >= 1

lab = CardMontePlanter()
garden_pass = lab.find_seeds(fire=PurgeFail(), maximum=sims)
garden_fail = lab.find_seeds(fire=PurgePass(), maximum=sims)

passes = len(garden_pass)
fails = len(garden_fail)

print(f"{sims} Sims => {passes + fails} Results | {passes} Pass, {fails} Fail")

odds = passes / (passes + fails)

print(f"Winning odds: {(odds * 100):.2f}%")

pass_seeds = [seed for seed, _ in garden_pass]

fire = PurgeFail()

for seed in pass_seeds:
    sprout = Sprout(seed)
    lab.plant(sprout)
    if fire.purge(sprout):
        raise Exception(f"Seed {seed} is supposed to pass, but is purged.")

print("All passing seeds re-passed purging.")