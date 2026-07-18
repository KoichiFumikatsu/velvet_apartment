import pytest
from velvet import economy


def test_affection_multiplier():
    assert economy.affection_multiplier(0) == 1.0
    assert economy.affection_multiplier(50) == 2.0
    assert economy.affection_multiplier(100) == 3.0


def test_facade_multiplier():
    assert economy.facade_multiplier(0) == 1.0
    assert economy.facade_multiplier(3) == pytest.approx(1.30)


def test_room_upgrade_cost():
    assert economy.room_upgrade_cost(0) == pytest.approx(10.0)
    assert economy.room_upgrade_cost(1) == pytest.approx(11.5)


def test_facade_cost():
    assert economy.facade_cost(0) == pytest.approx(100.0)
    assert economy.facade_cost(2) == pytest.approx(225.0)


def test_base_income_scales_per_floor():
    assert economy.base_income(0) == pytest.approx(1.0)
    assert economy.base_income(1) == pytest.approx(5.0)
    assert economy.base_income(2) == pytest.approx(25.0)
