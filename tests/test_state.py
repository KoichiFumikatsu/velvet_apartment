from velvet import state


def test_room_occupancy():
    r = state.Room()
    assert r.occupied is False
    r.guest = state.Guest(name="Amber-like")
    assert r.occupied is True


def test_new_game_starts_with_floor_zero():
    gs = state.new_game()
    assert gs.money == 0.0
    assert gs.facade_level == 0
    assert len(gs.floors) == 1
    assert gs.floors[0].index == 0
    assert gs.floors[0].unlocked is True
    assert len(gs.floors[0].rooms) == 3
    assert all(not room.occupied for room in gs.floors[0].rooms)
