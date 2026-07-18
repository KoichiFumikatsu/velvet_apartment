from __future__ import annotations

from velvet import config
from velvet.state import Floor, GameState, Guest, Room


def condition_cost(floor_index: int) -> float:
    return config.CONDITION_BASE * (config.CONDITION_FLOOR_MULT ** floor_index)


def repair_cost(floor_index: int) -> float:
    return config.REPAIR_BASE * (config.REPAIR_FLOOR_MULT ** floor_index)


def condition_room(gs: GameState, floor: Floor, room: Room, guest: Guest) -> bool:
    cost = condition_cost(floor.index)
    if gs.money < cost or room.occupied:
        return False
    gs.money -= cost
    room.guest = guest
    return True


def floor_full(floor: Floor) -> bool:
    return all(room.occupied for room in floor.rooms)


def unlock_next_floor(gs: GameState, floor: Floor) -> bool:
    if floor.repaired:
        return False
    if not floor_full(floor):
        return False
    cost = repair_cost(floor.index)
    if gs.money < cost:
        return False
    gs.money -= cost
    floor.repaired = True
    gs.floors.append(
        Floor(index=floor.index + 1, rooms=[Room(), Room(), Room()], unlocked=True)
    )
    return True
