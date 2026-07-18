import pytest
from velvet import hotel, state


def test_condition_room_assigns_guest():
    gs = state.new_game()
    gs.money = 100.0
    room = gs.floors[0].rooms[0]
    g = state.Guest(name="Amber-like")
    assert hotel.condition_room(gs, gs.floors[0], room, g) is True
    assert room.occupied is True
    assert gs.money == pytest.approx(90.0)  # condition_cost floor 0 = 10


def test_floor_full():
    gs = state.new_game()
    floor = gs.floors[0]
    assert hotel.floor_full(floor) is False
    for room in floor.rooms:
        room.guest = state.Guest(name="G")
    assert hotel.floor_full(floor) is True


def test_unlock_next_floor_requires_full_and_money():
    gs = state.new_game()
    floor = gs.floors[0]
    for room in floor.rooms:
        room.guest = state.Guest(name="G")
    assert hotel.unlock_next_floor(gs, floor) is False  # no money
    gs.money = 500.0
    assert hotel.unlock_next_floor(gs, floor) is True
    assert gs.money == pytest.approx(0.0)
    assert len(gs.floors) == 2
    assert gs.floors[1].index == 1
    assert gs.floors[1].unlocked is True
    assert len(gs.floors[1].rooms) == 3


def test_unlock_denied_when_not_full():
    gs = state.new_game()
    gs.money = 10_000.0
    assert hotel.unlock_next_floor(gs, gs.floors[0]) is False


def test_cost_scaling_per_floor():
    assert hotel.condition_cost(1) == pytest.approx(50.0)  # 10 * 5^1
    assert hotel.repair_cost(1) == pytest.approx(2000.0)  # 500 * 4^1


def test_unlock_next_floor_is_idempotent():
    gs = state.new_game()
    floor = gs.floors[0]
    for room in floor.rooms:
        room.guest = state.Guest(name="G")
    gs.money = 1000.0  # enough for two repairs at floor 0 (500 each)
    assert hotel.unlock_next_floor(gs, floor) is True
    assert hotel.unlock_next_floor(gs, floor) is False
    assert len(gs.floors) == 2
    assert gs.money == pytest.approx(500.0)
