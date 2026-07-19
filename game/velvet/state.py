from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Guest:
    name: str
    affection: float = 0.0
    services_bought: int = 0
    last_visit: float = 0.0


@dataclass
class Room:
    upgrade_level: int = 1
    guest: Guest | None = None

    @property
    def occupied(self) -> bool:
        return self.guest is not None


@dataclass
class Floor:
    index: int
    rooms: list[Room]
    unlocked: bool = False
    repaired: bool = False


@dataclass
class GameState:
    money: float = 0.0
    facade_level: int = 0
    last_seen: float = 0.0
    floors: list[Floor] = field(default_factory=list)
    tutorial_step: int = 0
    tutorial_done: bool = False


def new_game() -> GameState:
    floor0 = Floor(index=0, rooms=[Room(), Room(), Room()], unlocked=True)
    return GameState(floors=[floor0])
