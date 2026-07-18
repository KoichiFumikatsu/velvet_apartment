from __future__ import annotations

from velvet import affection, config, economy
from velvet.state import GameState, Guest, Room


def visit(guest: Guest, now: float) -> bool:
    if now - guest.last_visit < config.VISIT_COOLDOWN_SEC:
        return False
    affection.add_affection(guest, config.VISIT_GAIN)
    guest.last_visit = now
    return True


def service_cost(services_bought: int) -> float:
    return config.SERVICE_COST_BASE * (config.SERVICE_COST_GROWTH ** services_bought)


def buy_service(gs: GameState, guest: Guest) -> bool:
    cost = service_cost(guest.services_bought)
    if gs.money < cost:
        return False
    gs.money -= cost
    affection.add_affection(guest, config.SERVICE_GAIN)
    guest.services_bought += 1
    return True


def upgrade_room(gs: GameState, room: Room) -> bool:
    cost = economy.room_upgrade_cost(room.upgrade_level)
    if gs.money < cost:
        return False
    gs.money -= cost
    room.upgrade_level += 1
    return True


def upgrade_facade(gs: GameState) -> bool:
    cost = economy.facade_cost(gs.facade_level)
    if gs.money < cost:
        return False
    gs.money -= cost
    gs.facade_level += 1
    return True
