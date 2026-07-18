from __future__ import annotations

from velvet import affection, config
from velvet.state import Guest, Room

_TIER_NAMES = {
    "SFW": "SFW",
    "SUGGESTIVE": "Sugerente",
    "NSFW": "NSFW",
    "NSFW_NOCTURNO": "NSFW Nocturno",
}


def abbreviate(amount: float) -> str:
    n = float(amount)
    for suffix, size in (("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(n) >= size:
            return f"{n / size:.2f}{suffix}"
    return str(int(n))


def format_money(amount: float) -> str:
    return "$" + abbreviate(amount)


def affection_fraction(guest: Guest) -> float:
    return max(0.0, min(1.0, guest.affection / config.AFFECTION_MAX))


def tier_display(guest: Guest) -> str:
    return _TIER_NAMES[affection.current_tier(guest.affection)]


def door_label(room: Room) -> str:
    return room.guest.name if room.occupied else "Vacía"


def room_income_label(income_per_sec: float) -> str:
    return format_money(income_per_sec) + "/s"


def cost_label(cost: float) -> str:
    return format_money(cost)
