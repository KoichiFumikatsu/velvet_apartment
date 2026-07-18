import pytest
from velvet import config, economy, session, state


def _occupied_game():
    gs = state.new_game()
    gs.floors[0].rooms[0].guest = state.Guest(name="G", affection=0)  # income 1.0/s
    return gs


def test_apply_tick_accrues_money():
    gs = _occupied_game()
    session.apply_tick(gs, dt=10.0)
    assert gs.money == pytest.approx(10.0)


def test_catch_up_seeds_last_seen_first_time():
    gs = _occupied_game()
    credited = session.catch_up(gs, now=1000.0)
    assert credited == 0.0
    assert gs.last_seen == 1000.0
    assert gs.money == 0.0


def test_catch_up_credits_offline():
    gs = _occupied_game()
    gs.last_seen = 1000.0
    credited = session.catch_up(gs, now=1100.0)  # 100s * 1.0/s
    assert credited == pytest.approx(100.0)
    assert gs.money == pytest.approx(100.0)
    assert gs.last_seen == 1100.0


def test_catch_up_caps_at_offline_limit():
    gs = _occupied_game()
    gs.last_seen = 1000.0
    elapsed = config.OFFLINE_CAP_SEC + 3600.0  # 1h beyond the 8h cap
    now = gs.last_seen + elapsed
    income_per_sec = economy.total_income_per_sec(gs)
    credited = session.catch_up(gs, now=now)
    assert credited == pytest.approx(income_per_sec * config.OFFLINE_CAP_SEC)
    assert gs.money == pytest.approx(income_per_sec * config.OFFLINE_CAP_SEC)
    assert gs.last_seen == now
