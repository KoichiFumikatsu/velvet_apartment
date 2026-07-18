import pytest
from velvet import actions, state


def test_visit_respects_cooldown():
    g = state.Guest(name="G", last_visit=0.0)
    assert actions.visit(g, now=100.0) is True
    assert g.affection == 5.0
    assert actions.visit(g, now=130.0) is False  # < 60s later
    assert g.affection == 5.0
    assert actions.visit(g, now=161.0) is True
    assert g.affection == 10.0


def test_service_cost_grows():
    assert actions.service_cost(0) == pytest.approx(20.0)
    assert actions.service_cost(1) == pytest.approx(26.0)


def test_buy_service_requires_money():
    gs = state.new_game()
    g = state.Guest(name="G")
    assert actions.buy_service(gs, g) is False  # money 0
    gs.money = 100.0
    assert actions.buy_service(gs, g) is True
    assert gs.money == pytest.approx(80.0)
    assert g.affection == 10.0
    assert g.services_bought == 1
