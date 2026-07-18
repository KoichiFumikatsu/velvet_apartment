from __future__ import annotations

from velvet import config


def offline_earnings(income_per_sec: float, elapsed_sec: float) -> float:
    capped = min(max(elapsed_sec, 0.0), config.OFFLINE_CAP_SEC)
    return income_per_sec * capped


def clicker_reward(clicks: int, income_per_sec: float) -> float:
    seconds = min(config.CLICKER_INCOME_PER_CLICK * max(clicks, 0), config.CLICKER_CAP_SEC)
    return seconds * income_per_sec
