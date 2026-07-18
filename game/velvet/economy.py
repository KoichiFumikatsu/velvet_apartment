from __future__ import annotations

from velvet import config
from velvet.state import GameState, Room


def affection_multiplier(affection: float) -> float:
    return 1.0 + affection / config.AFFECTION_DIVISOR


def facade_multiplier(facade_level: int) -> float:
    return 1.0 + config.FACADE_BONUS_PER_LEVEL * facade_level


def room_upgrade_cost(level: int) -> float:
    return config.ROOM_UPGRADE_BASE * (config.ROOM_UPGRADE_GROWTH ** level)


def facade_cost(level: int) -> float:
    return config.FACADE_BASE * (config.FACADE_GROWTH ** level)


def base_income(floor_index: int) -> float:
    return config.BASE_INCOME_FLOOR1 * (config.FLOOR_INCOME_MULTIPLIER ** floor_index)


def room_income(room: Room, facade_level: int, floor_index: int) -> float:
    if not room.occupied:
        return 0.0
    return (
        base_income(floor_index)
        * room.upgrade_level
        * affection_multiplier(room.guest.affection)
        * facade_multiplier(facade_level)
    )


def total_income_per_sec(gs: GameState) -> float:
    total = 0.0
    for floor in gs.floors:
        if not floor.unlocked:
            continue
        for room in floor.rooms:
            total += room_income(room, gs.facade_level, floor.index)
    return total
