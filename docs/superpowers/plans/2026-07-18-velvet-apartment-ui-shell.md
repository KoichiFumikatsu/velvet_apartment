# Velvet Apartment — UI Shell (Incremento 1) — Implementation Plan

**Goal:** A runnable Ren'Py shell: main menu (night facade) → reception hub (first-person, point-and-click hotspots) with monitor/hallway/elevator functional against the engine, plus save/offline and stub panels — all with programmatic placeholder art.

**Architecture:** Standard Ren'Py GUI base (copied from SDK template) at 1920×1080, rollback off. `default gs = velvet.state.new_game()` in the store; screens read `gs` and call the pure engine API (`velvet.actions/hotel/session`). Pure display helpers in `game/velvet/display.py` (TDD). Navigation = hub label dispatching `renpy.call_screen`. Tick via `timer 1.0` → `apply_tick` + stamp `last_seen`; `catch_up` on load.

**Tech Stack:** Ren'Py 8.3.7 (SDK `C:\Users\fumik\renpy-8.3.7-sdk`), Python 3.12, pytest.

## Global Constraints
- `game/velvet/` engine modules stay pure (no `renpy` import); `display.py` too. All `.rpy` call the engine API — no game logic in `.rpy`.
- Placeholder art only: Ren'Py `Solid`/`Frame`/`Text`/`textbutton` with `hover_background`. No external image files (beyond the SDK template's default gui/ assets).
- Resolution 1920×1080; `config.rollback_enabled = False`.
- Verification per step: `renpy lint` clean; `pytest` green for `display.py` + engine (34 existing).
- Lint command: `cd /c/Users/fumik/renpy-8.3.7-sdk && ./renpy.exe "C:/Users/fumik/projects/velvet_apartment" lint`

## Tasks (executed inline by the controller; lint after each; commit per task)
1. **display.py + TDD** — `format_money`, `abbreviate`, `affection_fraction`, `tier_display`, `door_label`, `room_income_label`, `cost_label`. pytest.
2. **Base scaffold** — copy SDK `gui/game/*` into `game/` (keep `game/velvet/`); set `options.rpy` (name, 1920×1080 via gui.init, rollback off); `script.rpy` `label start` → seed/catch_up → `jump hub`. Lint + boots.
3. **bridge.rpy** — `default gs`, `default current_floor`, `default last_clicker`; `init python` helpers: `game_tick()`, `new_or_continue()`, placeholder guest factory. Lint.
4. **reception.rpy** — hub scene + hotspots (monitor/pasillo/ascensor/tablón/cajón) with hover, top bar money+income, `timer 1.0`. `hub` label dispatch. Lint.
5. **management.rpy** — monitor panel: Habitaciones tab (rooms of unlocked floors: label, affection bar, income, upgrade), Fachada tab (upgrade), Huéspedes tab, stub Cámaras/Históricos. Lint.
6. **hallway_room.rpy** — hallway (3 doors of current_floor; occupied→room, empty→condition_room w/ placeholder guest); room (affection bar, visit/service/upgrade, tier display, package→clicker). Lint.
7. **floors.rpy** — elevator: floors list, current, unlock next (repair). Lint.
8. **clicker.rpy** — package minigame (15s, click, reward via idle.clicker_reward, cooldown). Lint.
9. **stubs + main_menu** — `inventory`/`tasks` "en construcción"; night-facade main_menu reskin (Continuar/Nueva/Opciones/Salir). Final full lint + boot smoke. 

## Verification & handoff
- Headless: `renpy lint` clean + `pytest` green after each task.
- **Deferred to human (needs display):** launch the game and visually play-test — not verifiable in this headless session. Documented in the final summary.
- Final: opus whole-branch review, then merge to main.
