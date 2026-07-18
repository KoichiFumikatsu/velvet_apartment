from __future__ import annotations

# Economy
ROOM_UPGRADE_BASE = 10.0
ROOM_UPGRADE_GROWTH = 1.15
FACADE_BASE = 100.0
FACADE_GROWTH = 1.5
FACADE_BONUS_PER_LEVEL = 0.10          # +10% income per facade level
BASE_INCOME_FLOOR1 = 1.0               # $/s
FLOOR_INCOME_MULTIPLIER = 5.0          # ×5 base income per floor above the first

# Affection
AFFECTION_MIN = 0.0
AFFECTION_MAX = 100.0
AFFECTION_DIVISOR = 50.0               # multiplier = 1 + affection/50
VISIT_GAIN = 5.0
VISIT_COOLDOWN_SEC = 60.0
SERVICE_GAIN = 10.0
SERVICE_COST_BASE = 20.0
SERVICE_COST_GROWTH = 1.3

# Tier thresholds (affection)
TIER_THRESHOLDS = {"SFW": 0.0, "SUGGESTIVE": 25.0, "NSFW": 60.0, "NSFW_NOCTURNO": 90.0}

# Clicker
CLICKER_INCOME_PER_CLICK = 0.5         # seconds-of-income per click
CLICKER_CAP_SEC = 300.0                # reward capped at 5 min of income
CLICKER_SESSION_SEC = 15.0             # spec §4: clicker session duration
CLICKER_COOLDOWN_SEC = 600.0           # spec §4: 10-minute cooldown between sessions

# Offline
OFFLINE_CAP_SEC = 8 * 3600.0           # 8 hours

# Hotel
CONDITION_BASE = 10.0
CONDITION_FLOOR_MULT = 5.0
REPAIR_BASE = 500.0
REPAIR_FLOOR_MULT = 4.0
