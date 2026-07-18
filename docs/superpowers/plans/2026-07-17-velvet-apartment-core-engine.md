# Velvet Apartment — Core Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the pure-Python game-logic engine for Velvet Apartment (economy, rooms, affection/tiers, floors, offline earnings, clicker) — fully unit-tested, with no Ren'Py runtime dependency.

**Architecture:** All game logic lives in a plain Python package `game/velvet/` with **zero `renpy` imports**, so it runs under host `pytest` (Python 3.12) and is also importable by Ren'Py (which puts `game/` on its path). The later UI plan builds Ren'Py screens that drive this engine. Pure functions for formulas; small dataclasses for state; mutation helpers return success booleans.

**Tech Stack:** Python 3.12 (host, for tests) · pytest · Ren'Py 8.3.7 (consumer, later plan) · stdlib only for engine (no third-party runtime deps).

## Global Constraints

- Engine modules under `game/velvet/` MUST NOT `import renpy` or any Ren'Py API — keep them pure so tests run on host Python.
- Money is `float`; affection is `float` clamped to `[0, 100]`; timestamps are Unix seconds (`float`).
- All economic formulas and thresholds come from the spec `docs/superpowers/specs/2026-07-17-velvet-apartment-design.md` and are **tunable constants** defined in `game/velvet/config.py` — never hardcode a magic number inside logic; read it from config.
- Exact constant values (verbatim from spec): room upgrade cost `10 * 1.15**level`; facade cost `100 * 1.5**level`, facade `+10%`/level; affection multiplier `1 + affection/50`; base income floor-1 `1.0 $/s`, `×5` per floor above; tier thresholds SFW `0`, Suggestive `25`, NSFW `60`, NSFW Nocturno `90`; visit gain `+5`, cooldown `60 s`; service `+10` affection, cost `20 * 1.3**bought`; clicker `0.5 × income/s` per click, cap `300 s` of income; offline cap `8 h`.
- Python: use `from __future__ import annotations` at the top of every module (clean type hints on 3.12).

---

### Task 1: Package skeleton + test harness

**Files:**
- Create: `game/velvet/__init__.py`
- Create: `game/velvet/config.py`
- Create: `conftest.py`
- Create: `pytest.ini`
- Create: `tests/test_smoke.py`
- Modify: `.gitignore`

**Interfaces:**
- Produces: importable package `velvet`; `velvet.config` module exposing the tunable constants used by all later tasks.

- [ ] **Step 1: Create venv and install pytest**

Run:
```bash
cd /c/Users/fumik/projects/velvet_apartment
py -3.12 -m venv .venv
./.venv/Scripts/python -m pip install -q pytest
```
Expected: pytest installs without error.

- [ ] **Step 2: Add venv to .gitignore**

Append to `.gitignore`:
```
# Python
.venv/
__pycache__/
*.pyc
.pytest_cache/
```

- [ ] **Step 3: Create the package files**

`game/velvet/__init__.py`:
```python
from __future__ import annotations
```

`game/velvet/config.py`:
```python
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

# Offline
OFFLINE_CAP_SEC = 8 * 3600.0           # 8 hours
```

`conftest.py`:
```python
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "game"))
```

`pytest.ini`:
```ini
[pytest]
testpaths = tests
```

`tests/test_smoke.py`:
```python
from velvet import config


def test_config_imports():
    assert config.ROOM_UPGRADE_GROWTH == 1.15
    assert config.TIER_THRESHOLDS["NSFW_NOCTURNO"] == 90.0
```

- [ ] **Step 4: Run the smoke test**

Run: `./.venv/Scripts/python -m pytest tests/test_smoke.py -v`
Expected: PASS (1 passed).

- [ ] **Step 5: Commit**

```bash
git add .gitignore conftest.py pytest.ini game/velvet/__init__.py game/velvet/config.py tests/test_smoke.py
git commit -m "feat(engine): package skeleton + pytest harness + tunable config"
```

---

### Task 2: Economy formulas

**Files:**
- Create: `game/velvet/economy.py`
- Test: `tests/test_economy.py`

**Interfaces:**
- Consumes: `velvet.config`.
- Produces:
  - `affection_multiplier(affection: float) -> float`
  - `facade_multiplier(facade_level: int) -> float`
  - `room_upgrade_cost(level: int) -> float`
  - `facade_cost(level: int) -> float`
  - `base_income(floor_index: int) -> float`  (floor_index is 0-based; floor 1 = 0)

- [ ] **Step 1: Write the failing test**

`tests/test_economy.py`:
```python
import pytest
from velvet import economy


def test_affection_multiplier():
    assert economy.affection_multiplier(0) == 1.0
    assert economy.affection_multiplier(50) == 2.0
    assert economy.affection_multiplier(100) == 3.0


def test_facade_multiplier():
    assert economy.facade_multiplier(0) == 1.0
    assert economy.facade_multiplier(3) == pytest.approx(1.30)


def test_room_upgrade_cost():
    assert economy.room_upgrade_cost(0) == pytest.approx(10.0)
    assert economy.room_upgrade_cost(1) == pytest.approx(11.5)


def test_facade_cost():
    assert economy.facade_cost(0) == pytest.approx(100.0)
    assert economy.facade_cost(2) == pytest.approx(225.0)


def test_base_income_scales_per_floor():
    assert economy.base_income(0) == pytest.approx(1.0)
    assert economy.base_income(1) == pytest.approx(5.0)
    assert economy.base_income(2) == pytest.approx(25.0)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/Scripts/python -m pytest tests/test_economy.py -v`
Expected: FAIL (ModuleNotFoundError: velvet.economy).

- [ ] **Step 3: Write minimal implementation**

`game/velvet/economy.py`:
```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/Scripts/python -m pytest tests/test_economy.py -v`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit**

```bash
git add game/velvet/economy.py tests/test_economy.py
git commit -m "feat(engine): economy formulas (multipliers, costs, base income)"
```

---

### Task 3: State model

**Files:**
- Create: `game/velvet/state.py`
- Test: `tests/test_state.py`

**Interfaces:**
- Produces dataclasses:
  - `Guest(name: str, affection: float = 0.0, services_bought: int = 0, last_visit: float = 0.0)`
  - `Room(upgrade_level: int = 1, guest: Guest | None = None)` with property `occupied -> bool`
  - `Floor(index: int, rooms: list[Room], unlocked: bool = False, repaired: bool = False)`
  - `GameState(money: float = 0.0, facade_level: int = 0, last_seen: float = 0.0, floors: list[Floor] = [])`
  - `new_game() -> GameState` — builds floor 0 (unlocked) with 3 empty rooms, floors 1+ absent until unlocked.

- [ ] **Step 1: Write the failing test**

`tests/test_state.py`:
```python
from velvet import state


def test_room_occupancy():
    r = state.Room()
    assert r.occupied is False
    r.guest = state.Guest(name="Amber-like")
    assert r.occupied is True


def test_new_game_starts_with_floor_zero():
    gs = state.new_game()
    assert gs.money == 0.0
    assert gs.facade_level == 0
    assert len(gs.floors) == 1
    assert gs.floors[0].index == 0
    assert gs.floors[0].unlocked is True
    assert len(gs.floors[0].rooms) == 3
    assert all(not room.occupied for room in gs.floors[0].rooms)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/Scripts/python -m pytest tests/test_state.py -v`
Expected: FAIL (ModuleNotFoundError: velvet.state).

- [ ] **Step 3: Write minimal implementation**

`game/velvet/state.py`:
```python
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


def new_game() -> GameState:
    floor0 = Floor(index=0, rooms=[Room(), Room(), Room()], unlocked=True)
    return GameState(floors=[floor0])
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/Scripts/python -m pytest tests/test_state.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add game/velvet/state.py tests/test_state.py
git commit -m "feat(engine): state model (Guest, Room, Floor, GameState, new_game)"
```

---

### Task 4: Room income + total income per second

**Files:**
- Modify: `game/velvet/economy.py`
- Test: `tests/test_income.py`

**Interfaces:**
- Consumes: `Room`, `GameState`, `affection_multiplier`, `facade_multiplier`, `base_income`.
- Produces:
  - `room_income(room: Room, facade_level: int, floor_index: int) -> float` — `0.0` if empty.
  - `total_income_per_sec(gs: GameState) -> float` — sum over rooms of **unlocked** floors.

- [ ] **Step 1: Write the failing test**

`tests/test_income.py`:
```python
import pytest
from velvet import economy, state


def test_empty_room_yields_zero():
    assert economy.room_income(state.Room(), facade_level=0, floor_index=0) == 0.0


def test_room_income_applies_all_multipliers():
    room = state.Room(upgrade_level=2, guest=state.Guest(name="G", affection=50))
    # base(0)=1.0 * upgrade 2 * affection_mult(50)=2.0 * facade_mult(0)=1.0 = 4.0
    assert economy.room_income(room, facade_level=0, floor_index=0) == pytest.approx(4.0)


def test_total_income_only_counts_unlocked_floors():
    gs = state.new_game()
    gs.floors[0].rooms[0].guest = state.Guest(name="G", affection=0)  # mult 1.0
    locked = state.Floor(index=1, rooms=[state.Room(guest=state.Guest(name="X"))], unlocked=False)
    gs.floors.append(locked)
    # only floor 0 room 0: base 1.0 * upgrade 1 * affection 1.0 * facade 1.0 = 1.0
    assert economy.total_income_per_sec(gs) == pytest.approx(1.0)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/Scripts/python -m pytest tests/test_income.py -v`
Expected: FAIL (AttributeError: module 'velvet.economy' has no attribute 'room_income').

- [ ] **Step 3: Write minimal implementation**

Append to `game/velvet/economy.py`:
```python
from velvet.state import GameState, Room


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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/Scripts/python -m pytest tests/test_income.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add game/velvet/economy.py tests/test_income.py
git commit -m "feat(engine): room income + total income per second"
```

---

### Task 5: Affection tiers

**Files:**
- Create: `game/velvet/affection.py`
- Test: `tests/test_affection.py`

**Interfaces:**
- Consumes: `velvet.config`, `Guest`.
- Produces:
  - `current_tier(affection: float) -> str` — one of `"SFW" | "SUGGESTIVE" | "NSFW" | "NSFW_NOCTURNO"`.
  - `unlocked_tiers(affection: float) -> list[str]` — all tiers at/under current affection, in order.
  - `add_affection(guest: Guest, amount: float) -> None` — clamps to `[0, 100]`.

- [ ] **Step 1: Write the failing test**

`tests/test_affection.py`:
```python
from velvet import affection, state


def test_current_tier_boundaries():
    assert affection.current_tier(0) == "SFW"
    assert affection.current_tier(24) == "SFW"
    assert affection.current_tier(25) == "SUGGESTIVE"
    assert affection.current_tier(60) == "NSFW"
    assert affection.current_tier(90) == "NSFW_NOCTURNO"
    assert affection.current_tier(100) == "NSFW_NOCTURNO"


def test_unlocked_tiers_accumulate():
    assert affection.unlocked_tiers(0) == ["SFW"]
    assert affection.unlocked_tiers(61) == ["SFW", "SUGGESTIVE", "NSFW"]


def test_add_affection_clamps():
    g = state.Guest(name="G", affection=95)
    affection.add_affection(g, 20)
    assert g.affection == 100.0
    affection.add_affection(g, -500)
    assert g.affection == 0.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/Scripts/python -m pytest tests/test_affection.py -v`
Expected: FAIL (ModuleNotFoundError: velvet.affection).

- [ ] **Step 3: Write minimal implementation**

`game/velvet/affection.py`:
```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/Scripts/python -m pytest tests/test_affection.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add game/velvet/affection.py tests/test_affection.py
git commit -m "feat(engine): affection tiers (current_tier, unlocked_tiers, add_affection)"
```

---

### Task 6: Visits (cooldown) + paid services

**Files:**
- Create: `game/velvet/actions.py`
- Test: `tests/test_actions.py`

**Interfaces:**
- Consumes: `velvet.config`, `velvet.affection`, `Guest`, `GameState`.
- Produces:
  - `visit(guest: Guest, now: float) -> bool` — if `now - guest.last_visit >= cooldown`, add `VISIT_GAIN`, set `last_visit = now`, return `True`; else `False`.
  - `service_cost(services_bought: int) -> float` — `20 * 1.3**bought`.
  - `buy_service(gs: GameState, guest: Guest) -> bool` — if `gs.money >= service_cost`, deduct, add `SERVICE_GAIN`, increment `services_bought`, return `True`; else `False`.

- [ ] **Step 1: Write the failing test**

`tests/test_actions.py`:
```python
import pytest
from velvet import actions, state


def test_visit_respects_cooldown():
    g = state.Guest(name="G", last_visit=0.0)
    assert actions.visit(g, now=100.0) is True
    assert g.affection == 5.0
    assert actions.visit(g, now=130.0) is False  # < 60s later
    assert g.affection == 5.0
    assert actions.visit(g, now=161.0) is True
    assert g.affection == 10.0


def test_service_cost_grows():
    assert actions.service_cost(0) == pytest.approx(20.0)
    assert actions.service_cost(1) == pytest.approx(26.0)


def test_buy_service_requires_money():
    gs = state.new_game()
    g = state.Guest(name="G")
    assert actions.buy_service(gs, g) is False  # money 0
    gs.money = 100.0
    assert actions.buy_service(gs, g) is True
    assert gs.money == pytest.approx(80.0)
    assert g.affection == 10.0
    assert g.services_bought == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/Scripts/python -m pytest tests/test_actions.py -v`
Expected: FAIL (ModuleNotFoundError: velvet.actions).

- [ ] **Step 3: Write minimal implementation**

`game/velvet/actions.py`:
```python
from __future__ import annotations

from velvet import affection, config
from velvet.state import GameState, Guest


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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/Scripts/python -m pytest tests/test_actions.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add game/velvet/actions.py tests/test_actions.py
git commit -m "feat(engine): visits with cooldown + paid services"
```

---

### Task 7: Room upgrades + facade purchases

**Files:**
- Modify: `game/velvet/actions.py`
- Test: `tests/test_upgrades.py`

**Interfaces:**
- Consumes: `velvet.economy`, `Room`, `GameState`.
- Produces:
  - `upgrade_room(gs: GameState, room: Room) -> bool` — cost `room_upgrade_cost(room.upgrade_level)`; on success deduct and `upgrade_level += 1`.
  - `upgrade_facade(gs: GameState) -> bool` — cost `facade_cost(gs.facade_level)`; on success deduct and `facade_level += 1`.

- [ ] **Step 1: Write the failing test**

`tests/test_upgrades.py`:
```python
import pytest
from velvet import actions, state


def test_upgrade_room_deducts_and_increments():
    gs = state.new_game()
    room = gs.floors[0].rooms[0]  # upgrade_level 1
    gs.money = 20.0
    assert actions.upgrade_room(gs, room) is True
    assert room.upgrade_level == 2
    assert gs.money == pytest.approx(20.0 - 11.5)  # cost at level 1


def test_upgrade_room_denied_without_money():
    gs = state.new_game()
    room = gs.floors[0].rooms[0]
    assert actions.upgrade_room(gs, room) is False
    assert room.upgrade_level == 1


def test_upgrade_facade():
    gs = state.new_game()
    gs.money = 100.0
    assert actions.upgrade_facade(gs) is True
    assert gs.facade_level == 1
    assert gs.money == pytest.approx(0.0)
    assert actions.upgrade_facade(gs) is False  # 150 needed, 0 left
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/Scripts/python -m pytest tests/test_upgrades.py -v`
Expected: FAIL (AttributeError: module 'velvet.actions' has no attribute 'upgrade_room').

- [ ] **Step 3: Write minimal implementation**

Append to `game/velvet/actions.py`:
```python
from velvet import economy
from velvet.state import Room


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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/Scripts/python -m pytest tests/test_upgrades.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add game/velvet/actions.py tests/test_upgrades.py
git commit -m "feat(engine): room + facade upgrade purchases"
```

---

### Task 8: Hotel — guest arrival + floor unlock wall

**Files:**
- Create: `game/velvet/hotel.py`
- Test: `tests/test_hotel.py`

**Interfaces:**
- Consumes: `velvet.config`, `velvet.economy`, `Room`, `Floor`, `GameState`, `Guest`.
- Produces:
  - `condition_cost(floor_index: int) -> float` — cost to condition a room so a guest arrives; `room_upgrade_cost(0)` scaled by floor: `10 * 5**floor_index`.
  - `condition_room(gs: GameState, floor: Floor, room: Room, guest: Guest) -> bool` — pay `condition_cost`, assign `guest` to `room`.
  - `repair_cost(floor_index: int) -> float` — `500 * 4**floor_index`.
  - `floor_full(floor: Floor) -> bool` — all rooms occupied.
  - `unlock_next_floor(gs: GameState, floor: Floor) -> bool` — requires `floor_full` and `gs.money >= repair_cost(floor.index)`; on success deduct, append a new locked→unlocked `Floor(index+1)` with 3 empty rooms, return `True`.

- [ ] **Step 1: Write the failing test**

`tests/test_hotel.py`:
```python
import pytest
from velvet import hotel, state


def test_condition_room_assigns_guest():
    gs = state.new_game()
    gs.money = 100.0
    room = gs.floors[0].rooms[0]
    g = state.Guest(name="Amber-like")
    assert hotel.condition_room(gs, gs.floors[0], room, g) is True
    assert room.occupied is True
    assert gs.money == pytest.approx(90.0)  # condition_cost floor 0 = 10


def test_floor_full():
    gs = state.new_game()
    floor = gs.floors[0]
    assert hotel.floor_full(floor) is False
    for room in floor.rooms:
        room.guest = state.Guest(name="G")
    assert hotel.floor_full(floor) is True


def test_unlock_next_floor_requires_full_and_money():
    gs = state.new_game()
    floor = gs.floors[0]
    for room in floor.rooms:
        room.guest = state.Guest(name="G")
    assert hotel.unlock_next_floor(gs, floor) is False  # no money
    gs.money = 500.0
    assert hotel.unlock_next_floor(gs, floor) is True
    assert gs.money == pytest.approx(0.0)
    assert len(gs.floors) == 2
    assert gs.floors[1].index == 1
    assert gs.floors[1].unlocked is True
    assert len(gs.floors[1].rooms) == 3


def test_unlock_denied_when_not_full():
    gs = state.new_game()
    gs.money = 10_000.0
    assert hotel.unlock_next_floor(gs, gs.floors[0]) is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/Scripts/python -m pytest tests/test_hotel.py -v`
Expected: FAIL (ModuleNotFoundError: velvet.hotel).

- [ ] **Step 3: Write minimal implementation**

`game/velvet/hotel.py`:
```python
from __future__ import annotations

from velvet.state import Floor, GameState, Guest, Room

CONDITION_BASE = 10.0
CONDITION_FLOOR_MULT = 5.0
REPAIR_BASE = 500.0
REPAIR_FLOOR_MULT = 4.0


def condition_cost(floor_index: int) -> float:
    return CONDITION_BASE * (CONDITION_FLOOR_MULT ** floor_index)


def repair_cost(floor_index: int) -> float:
    return REPAIR_BASE * (REPAIR_FLOOR_MULT ** floor_index)


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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/Scripts/python -m pytest tests/test_hotel.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add game/velvet/hotel.py tests/test_hotel.py
git commit -m "feat(engine): guest arrival + floor unlock wall"
```

---

### Task 9: Offline earnings + clicker reward

**Files:**
- Create: `game/velvet/idle.py`
- Test: `tests/test_idle.py`

**Interfaces:**
- Consumes: `velvet.config`.
- Produces:
  - `offline_earnings(income_per_sec: float, elapsed_sec: float) -> float` — `income * min(max(elapsed,0), OFFLINE_CAP_SEC)`.
  - `clicker_reward(clicks: int, income_per_sec: float) -> float` — `min(CLICKER_INCOME_PER_CLICK * max(clicks,0), CLICKER_CAP_SEC) * income_per_sec`.

- [ ] **Step 1: Write the failing test**

`tests/test_idle.py`:
```python
import pytest
from velvet import idle


def test_offline_earnings_capped_at_8h():
    assert idle.offline_earnings(2.0, 100.0) == pytest.approx(200.0)
    capped = idle.offline_earnings(2.0, 100_000.0)  # > 8h
    assert capped == pytest.approx(2.0 * 8 * 3600)


def test_offline_negative_elapsed_is_zero():
    assert idle.offline_earnings(5.0, -10.0) == 0.0


def test_clicker_reward_and_cap():
    assert idle.clicker_reward(10, 3.0) == pytest.approx(0.5 * 10 * 3.0)  # 15
    capped = idle.clicker_reward(100_000, 3.0)  # 0.5*100000 = 50000s > 300s cap
    assert capped == pytest.approx(300.0 * 3.0)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/Scripts/python -m pytest tests/test_idle.py -v`
Expected: FAIL (ModuleNotFoundError: velvet.idle).

- [ ] **Step 3: Write minimal implementation**

`game/velvet/idle.py`:
```python
from __future__ import annotations

from velvet import config


def offline_earnings(income_per_sec: float, elapsed_sec: float) -> float:
    capped = min(max(elapsed_sec, 0.0), config.OFFLINE_CAP_SEC)
    return income_per_sec * capped


def clicker_reward(clicks: int, income_per_sec: float) -> float:
    seconds = min(config.CLICKER_INCOME_PER_CLICK * max(clicks, 0), config.CLICKER_CAP_SEC)
    return seconds * income_per_sec
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/Scripts/python -m pytest tests/test_idle.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add game/velvet/idle.py tests/test_idle.py
git commit -m "feat(engine): offline earnings + clicker reward"
```

---

### Task 10: Tick + session integration (apply income over time, catch-up on load)

**Files:**
- Create: `game/velvet/session.py`
- Test: `tests/test_session.py`

**Interfaces:**
- Consumes: `velvet.economy`, `velvet.idle`, `GameState`.
- Produces:
  - `apply_tick(gs: GameState, dt: float) -> None` — `gs.money += total_income_per_sec(gs) * dt`.
  - `catch_up(gs: GameState, now: float) -> float` — credits offline earnings for `now - gs.last_seen` (capped), adds to money, sets `gs.last_seen = now`, returns amount credited. If `gs.last_seen == 0`, seed it to `now` and credit `0`.

- [ ] **Step 1: Write the failing test**

`tests/test_session.py`:
```python
import pytest
from velvet import session, state


def _occupied_game():
    gs = state.new_game()
    gs.floors[0].rooms[0].guest = state.Guest(name="G", affection=0)  # income 1.0/s
    return gs


def test_apply_tick_accrues_money():
    gs = _occupied_game()
    session.apply_tick(gs, dt=10.0)
    assert gs.money == pytest.approx(10.0)


def test_catch_up_seeds_last_seen_first_time():
    gs = _occupied_game()
    credited = session.catch_up(gs, now=1000.0)
    assert credited == 0.0
    assert gs.last_seen == 1000.0
    assert gs.money == 0.0


def test_catch_up_credits_offline():
    gs = _occupied_game()
    gs.last_seen = 1000.0
    credited = session.catch_up(gs, now=1100.0)  # 100s * 1.0/s
    assert credited == pytest.approx(100.0)
    assert gs.money == pytest.approx(100.0)
    assert gs.last_seen == 1100.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/Scripts/python -m pytest tests/test_session.py -v`
Expected: FAIL (ModuleNotFoundError: velvet.session).

- [ ] **Step 3: Write minimal implementation**

`game/velvet/session.py`:
```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/Scripts/python -m pytest tests/test_session.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Run the full suite + commit**

Run: `./.venv/Scripts/python -m pytest -v`
Expected: PASS (all tasks' tests green).

```bash
git add game/velvet/session.py tests/test_session.py
git commit -m "feat(engine): income tick + offline catch-up on load"
```

---

## Coverage note (engine plan vs. full MVP)

This plan delivers the **testable engine only**. The following MVP pieces are **out of scope here** and get their own plans next:
- **Ren'Py UI plan** — hotel screen, room screen, upgrades, gallery, clicker minigame screen, `timer 1.0` tick wiring, save/load integration (`catch_up` on load).
- **Content/data plan** — the 3 floor-1 guests as data + their SFW/Suggestive/NSFW/NSFW-Nocturno CG sets and events; gallery persistence; package→clicker event.
- **Narrative plan** — VN intro (unemployed → interview → wake in lobby → signed contract → first guest tutorial).

The engine's public API (`economy`, `affection`, `actions`, `hotel`, `idle`, `session`, `state`) is the contract those plans consume.
