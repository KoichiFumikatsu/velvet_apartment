import pytest
from velvet import idle


def test_offline_earnings_capped_at_8h():
    assert idle.offline_earnings(2.0, 100.0) == pytest.approx(200.0)
    capped = idle.offline_earnings(2.0, 100_000.0)  # > 8h
    assert capped == pytest.approx(2.0 * 8 * 3600)


def test_offline_negative_elapsed_is_zero():
    assert idle.offline_earnings(5.0, -10.0) == 0.0


def test_clicker_reward_and_cap():
    assert idle.clicker_reward(10, 3.0) == pytest.approx(0.5 * 10 * 3.0)  # 15
    capped = idle.clicker_reward(100_000, 3.0)  # 0.5*100000 = 50000s > 300s cap
    assert capped == pytest.approx(300.0 * 3.0)
