from seedler.Sprout import Sprout

def test_sprout_buds() -> None:
    sprout = Sprout(0)

    for count in range(100):
        state = "odd" if count % 2 != 0 else "even"
        sprout.add_bud(state)

    assert sprout.get_count("odd") == 50
    assert sprout.get_count("even") == 50

def test_sprout_growth() -> None:
    sprout = Sprout(0)

    for count in range(100):
        val = sprout.growth(count, count)
        sprout.add_bud(str(val))

    total_count = 0
    for count in range(100):
        total_count += sprout.get_count(str(count))

    assert total_count == 100

def test_spout_growth_limit() -> None:
    sprout = Sprout(0)

    for count in range(100):
        val = sprout.growth(0, 1)
        sprout.add_bud(str(val))

    total_count = sprout.get_count("0") + sprout.get_count("1")
    assert total_count == 100