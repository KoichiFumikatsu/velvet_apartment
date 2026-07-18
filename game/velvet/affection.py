from __future__ import annotations

from velvet import config
from velvet.state import Guest

# Tiers ordered by ascending threshold.
_ORDERED = sorted(config.TIER_THRESHOLDS.items(), key=lambda kv: kv[1])


def current_tier(affection: float) -> str:
    result = _ORDERED[0][0]
    for name, threshold in _ORDERED:
        if affection >= threshold:
            result = name
    return result


def unlocked_tiers(affection: float) -> list[str]:
    return [name for name, threshold in _ORDERED if affection >= threshold]


def add_affection(guest: Guest, amount: float) -> None:
    guest.affection = max(
        config.AFFECTION_MIN, min(config.AFFECTION_MAX, guest.affection + amount)
    )
