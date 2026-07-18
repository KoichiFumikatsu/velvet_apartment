import pytest
from velvet import economy, state


def test_empty_room_yields_zero():
    assert economy.room_income(state.Room(), facade_level=0, floor_index=0) == 0.0


def test_room_income_applies_all_multipliers():
    room = state.Room(upgrade_level=2, guest=state.Guest(name="G", affection=50))
    # base(0)=1.0 * upgrade 2 * affection_mult(50)=2.0 * facade_mult(0)=1.0 = 4.0
    assert economy.room_income(room, facade_level=0, floor_index=0) == pytest.approx(4.0)


def test_total_income_only_counts_unlocked_floors():
    gs = state.new_game()
    gs.floors[0].rooms[0].guest = state.Guest(name="G", affection=0)  # mult 1.0
    locked = state.Floor(index=1, rooms=[state.Room(guest=state.Guest(name="X"))], unlocked=False)
    gs.floors.append(locked)
    # only floor 0 room 0: base 1.0 * upgrade 1 * affection 1.0 * facade 1.0 = 1.0
    assert economy.total_income_per_sec(gs) == pytest.approx(1.0)


def test_total_income_two_rooms_with_facade_and_affection():
    gs = state.new_game()
    gs.facade_level = 1
    gs.floors[0].rooms[0].guest = state.Guest(name="A", affection=50)
    gs.floors[0].rooms[1].guest = state.Guest(name="B", affection=0)
    # room A: 1.0 * 1 * (1 + 50/50=2) * (1 + 0.1=1.1) = 2.2
    # room B: 1.0 * 1 * 1 * 1.1 = 1.1
    # total: 3.3
    assert economy.total_income_per_sec(gs) == pytest.approx(3.3)
