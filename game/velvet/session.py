from __future__ import annotations

from velvet import economy, idle
from velvet.state import GameState


def apply_tick(gs: GameState, dt: float) -> None:
    gs.money += economy.total_income_per_sec(gs) * dt


def catch_up(gs: GameState, now: float) -> float:
    if gs.last_seen == 0.0:
        gs.last_seen = now
        return 0.0
    elapsed = now - gs.last_seen
    credited = idle.offline_earnings(economy.total_income_per_sec(gs), elapsed)
    gs.money += credited
    gs.last_seen = now
    return credited
