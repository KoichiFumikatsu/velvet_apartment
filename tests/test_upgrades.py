import pytest
from velvet import actions, state


def test_upgrade_room_deducts_and_increments():
    gs = state.new_game()
    room = gs.floors[0].rooms[0]  # upgrade_level 1
    gs.money = 20.0
    assert actions.upgrade_room(gs, room) is True
    assert room.upgrade_level == 2
    assert gs.money == pytest.approx(20.0 - 11.5)  # cost at level 1


def test_upgrade_room_denied_without_money():
    gs = state.new_game()
    room = gs.floors[0].rooms[0]
    assert actions.upgrade_room(gs, room) is False
    assert room.upgrade_level == 1


def test_upgrade_facade():
    gs = state.new_game()
    gs.money = 100.0
    assert actions.upgrade_facade(gs) is True
    assert gs.facade_level == 1
    assert gs.money == pytest.approx(0.0)
    assert actions.upgrade_facade(gs) is False  # 150 needed, 0 left
