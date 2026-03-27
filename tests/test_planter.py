from seedler.Planter import Planter
from seedler.Sprout import Sprout

def test_planter() -> None:
    planter = Planter()

    for i in range(100):
        sprout = Sprout(i)
        sprout.add_bud(str(i))
        planter.add_seed(sprout)

    # test results are stored from sprouts
    mask = planter.df.apply(
        lambda row: (
            len(row["results"]) == 1 and
            next(iter(row["results"].keys())) == str(row.name) and
            next(iter(row["results"].values())) == 1
        ),
        axis = 1
    )

    assert len(planter.df) == 100
    assert mask.all()