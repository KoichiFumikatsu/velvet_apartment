from __future__ import annotations

from velvet import config


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
