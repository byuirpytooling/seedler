# 3-Card Monte Simulation

**Key Learning:**
- Using seedler `Planter`, `Sprout`, and `Fire` classes
- Using flags for buds
- Monte-Carlo probability simulation
- Re-simulating seeds

## Simulation Baseline

The classic 3-card monte game is where the player is presented with 3 face-down cards - two losing, one winning - and must select on card. The standard odds, without cheating is easy to know since 1/3 of cards are winning, which means the player wins 33.33% of the time. However, we can use `seedler` to run a monte-carlo simulation of the situation to get a similar answer.

=== "Python"
    ```python
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
    print(f"Winning odds: {(odds * 100):.2f}%")
    ```

=== "Expected Output"
    ```text
    100 Sims => 100 Results | 32 Pass, 68 Fail
    Winning odds: 32.00%
    ```

In this simple example, we calculate our winning odds at 32%, which for 100 tests is very close to the true answer. The power comes when we simulate more complex problems, and simulate thousands or millions of times.


## Re-Simulating Single Seeds

Here is a brief example on re-simulating single seeds for results.

```python
sprout = Sprout(seed)
lab.plant(sprout)
is_purged = fire.purge(sprout)
```

Where lab is a `Planter`, and fire is a `Fire`.

Below, we run the 3-card monte, and re-simulate all passing results one-at-a-time to re-check the results.

=== "Python"
    ```python
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

    fire = PurgeFail()
    lab = CardMontePlanter()
    garden_pass = lab.find_seeds(fire=fire, maximum=sims)

    pass_seeds = [seed for seed, _ in garden_pass]

    for seed in pass_seeds:
        sprout = Sprout(seed)
        lab.plant(sprout)
        if fire.purge(sprout):
            raise Exception(f"Seed {seed} is supposed to pass, but is purged.")

    print("All passing seeds re-passed purging.")
    ```

=== "Expected Output"
    ```text
    All passing seeds re-passed purging.
    ```
