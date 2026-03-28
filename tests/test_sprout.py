from seedler import Sprout


def test_sprout_buds() -> None:
    sprout = Sprout(0)

    ODD = 0
    EVEN = 1

    for count in range(100):
        state = ODD if count % 2 != 0 else EVEN
        sprout.add_bud(state)

    assert sprout.get_bud_count(ODD) == 50
    assert sprout.get_bud_count(EVEN) == 50


def test_sprout_growth() -> None:
    sprout = Sprout(0)

    for count in range(100):
        val = sprout.growth(count, count)
        sprout.add_bud(val)

    res = sprout.to_dict()

    assert sum(res.values()) == 100


def test_spout_growth_limit() -> None:
    sprout = Sprout(0)

    for count in range(100):
        val = sprout.growth(0, 1)
        sprout.add_bud(val)

    res = sprout.to_dict()
    total_count = res[0] + res[1]

    assert total_count == 100


def test_sprout_get_results() -> None:
    sprout = Sprout(0)

    for _ in range(100):
        val = sprout.growth(0, 100)
        sprout.add_bud(val, 1)
    
    total_count = sum(sprout.to_dict().values())
    
    assert total_count == 100