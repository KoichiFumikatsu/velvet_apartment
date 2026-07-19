# Incremento Narrativa — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reemplazar el stub de 1 línea en `label start` por una intro VN cómica lineal que siembra a Amber en la habitación 1 y arranca un tutorial de objetivos con seguimiento.

**Architecture:** Ren'Py ya es motor VN — la narrativa es contenido `.rpy` (labels/`say`/`character`). La única lógica nueva es un rastreador de tutorial **puro** (`game/velvet/tutorial.py`) y los datos de Amber (`game/velvet/guests.py`), ambos sin `import renpy` y testeables con pytest. El panel de objetivos y el aviso de fin se dibujan con los patrones ya establecidos (DynamicDisplayable, notify).

**Tech Stack:** Ren'Py 8.3.7, Python puro (motor), pytest (`.venv`), framework `renpy test` (runtime headless).

## Global Constraints

- **Motor puro**: `game/velvet/*.py` NUNCA hace `import renpy`. Todo lo importable y testeable con pytest.
- **Tunables en `config.py`**: ningún número mágico nuevo fuera de config (los textos narrativos sí viven en su módulo/`.rpy`).
- **Nombre de Amber en un solo lugar**: `guests.AMBER_NAME`. Ningún `.rpy` hardcodea la cadena `"Amber"` para lógica (los diálogos donde el personaje se llama a sí mismo son texto, no lógica).
- **Riesgo legal Amber/HoYoverse**: override consciente de Koichi (registrado en el spec). No re-litigar.
- **Trampas Ren'Py** (de `docs/ESTADO.md`): mutadores del motor van por `act()`; usar `Return("back")`/centinela, nunca `Return(None)` cuando el valor se usa; escapar `[[ ]]` y `{{ }}` en texto literal; `timer 1.0 action Function(game_tick, _update_screens=False)`.
- **Verificación**: pytest para módulos puros; `renpy lint` + `renpy test flow` para `.rpy`.
- Comandos:
  - pytest: `./.venv/Scripts/python.exe -m pytest -q`
  - lint: `cd /c/Users/fumik/renpy-8.3.7-sdk && ./renpy.exe "C:/Users/fumik/projects/velvet_apartment" lint`
  - runtime: `cd /c/Users/fumik/renpy-8.3.7-sdk && ./renpy.exe "C:/Users/fumik/projects/velvet_apartment" test flow`

---

### Task 1: Rastreador de tutorial (motor puro)

**Files:**
- Modify: `game/velvet/state.py` (agregar 2 campos a `GameState`)
- Create: `game/velvet/tutorial.py`
- Test: `tests/test_tutorial.py`

**Interfaces:**
- Consumes: `state.GameState` (`.floors[0].rooms[0]`, `.tutorial_step`, `.tutorial_done`), `state.Guest.affection`, `state.Room.upgrade_level`.
- Produces:
  - `state.GameState.tutorial_step: int = 0`
  - `state.GameState.tutorial_done: bool = False`
  - `tutorial.STEPS: list[tuple[str, callable]]`
  - `tutorial.advance(gs) -> bool` (True solo en la transición que completa el tutorial)
  - `tutorial.current_text(gs) -> str | None`

- [ ] **Step 1: Write the failing test**

`tests/test_tutorial.py`:
```python
from velvet import state, tutorial


def _fresh():
    gs = state.new_game()
    gs.floors[0].rooms[0].guest = state.Guest(name="Amber")
    return gs


def test_starts_at_first_step():
    gs = _fresh()
    assert gs.tutorial_step == 0
    assert gs.tutorial_done is False
    assert tutorial.current_text(gs) == tutorial.STEPS[0][0]


def test_advances_after_visit():
    gs = _fresh()
    assert tutorial.advance(gs) is False          # nada hecho aún
    assert gs.tutorial_step == 0
    gs.floors[0].rooms[0].guest.affection = 5.0    # visitó
    assert tutorial.advance(gs) is False           # pasa a paso 1, no completa
    assert gs.tutorial_step == 1
    assert tutorial.current_text(gs) == tutorial.STEPS[1][0]


def test_completes_after_upgrade():
    gs = _fresh()
    gs.floors[0].rooms[0].guest.affection = 5.0
    gs.floors[0].rooms[0].upgrade_level = 2
    assert tutorial.advance(gs) is True            # transición a completo
    assert gs.tutorial_done is True
    assert tutorial.current_text(gs) is None


def test_does_not_skip_steps():
    gs = _fresh()
    gs.floors[0].rooms[0].upgrade_level = 2         # upgrade sin visitar primero
    assert tutorial.advance(gs) is False
    assert gs.tutorial_step == 0                     # el gate del paso 0 no se cumplió


def test_idempotent_when_done():
    gs = _fresh()
    gs.tutorial_done = True
    assert tutorial.advance(gs) is False
    assert tutorial.current_text(gs) is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/Scripts/python.exe -m pytest tests/test_tutorial.py -q`
Expected: FAIL (`ModuleNotFoundError: velvet.tutorial` / `GameState` sin `tutorial_step`).

- [ ] **Step 3: Add the GameState fields**

En `game/velvet/state.py`, dentro de `@dataclass class GameState`, agregar debajo de `last_seen`:
```python
    tutorial_step: int = 0
    tutorial_done: bool = False
```
(Campos con default → no rompe `new_game()` ni saves/tests previos.)

- [ ] **Step 4: Write minimal implementation**

`game/velvet/tutorial.py`:
```python
from __future__ import annotations

from velvet.state import GameState


def _room0(gs: GameState):
    return gs.floors[0].rooms[0]


def _visited(gs: GameState) -> bool:
    r = _room0(gs)
    return r.guest is not None and r.guest.affection > 0


def _upgraded(gs: GameState) -> bool:
    return _room0(gs).upgrade_level > 1


# Pasos accionables del tutorial (texto, gate). El cierre se emite al completar.
STEPS = [
    ("Abrí el Pasillo y visitá a Amber.", _visited),
    ("Con lo que genera, mejorá su habitación.", _upgraded),
]


def current_text(gs: GameState) -> str | None:
    if gs.tutorial_done or gs.tutorial_step >= len(STEPS):
        return None
    return STEPS[gs.tutorial_step][0]


def advance(gs: GameState) -> bool:
    """Avanza por los pasos ya cumplidos. Devuelve True SOLO en la
    transición que completa el tutorial (para disparar el aviso de fin)."""
    if gs.tutorial_done:
        return False
    while gs.tutorial_step < len(STEPS) and STEPS[gs.tutorial_step][1](gs):
        gs.tutorial_step += 1
    if gs.tutorial_step >= len(STEPS):
        gs.tutorial_done = True
        return True
    return False
```

- [ ] **Step 5: Run test to verify it passes**

Run: `./.venv/Scripts/python.exe -m pytest tests/test_tutorial.py -q`
Expected: PASS (5 passed).

- [ ] **Step 6: Full suite green**

Run: `./.venv/Scripts/python.exe -m pytest -q`
Expected: PASS (todos los previos + los nuevos).

- [ ] **Step 7: Commit**

```bash
git add game/velvet/state.py game/velvet/tutorial.py tests/test_tutorial.py
git commit -m "feat(engine): rastreador de tutorial puro + campos tutorial_step/done"
```

---

### Task 2: Amber como datos (motor puro)

**Files:**
- Create: `game/velvet/guests.py`
- Test: `tests/test_guests.py`

**Interfaces:**
- Consumes: `state.Guest`, `affection.current_tier(affection: float) -> str`, `config.TIER_THRESHOLDS`.
- Produces:
  - `guests.AMBER_NAME: str` (= `"Amber"`)
  - `guests.AMBER_LINES: dict[str, str]` (claves = tiers de `config.TIER_THRESHOLDS`)
  - `guests.make_amber() -> state.Guest`
  - `guests.amber_visit_line(affection: float) -> str`

- [ ] **Step 1: Write the failing test**

`tests/test_guests.py`:
```python
from velvet import guests


def test_amber_name_single_source():
    g = guests.make_amber()
    assert g.name == guests.AMBER_NAME == "Amber"
    assert g.affection == 0.0


def test_visit_line_by_tier():
    assert guests.amber_visit_line(0.0) == guests.AMBER_LINES["SFW"]
    assert guests.amber_visit_line(30.0) == guests.AMBER_LINES["SUGGESTIVE"]


def test_lines_cover_all_tiers():
    from velvet import config
    assert set(guests.AMBER_LINES) == set(config.TIER_THRESHOLDS)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/Scripts/python.exe -m pytest tests/test_guests.py -q`
Expected: FAIL (`ModuleNotFoundError: velvet.guests`).

- [ ] **Step 3: Write minimal implementation**

`game/velvet/guests.py`:
```python
from __future__ import annotations

from velvet import affection
from velvet.state import Guest

# Único lugar donde vive el nombre (trivial de cambiar si se retira el override legal).
AMBER_NAME = "Amber"

# Líneas de saludo/visita por tier (datos). NSFW/Nocturno son stubs: el incremento
# de Contenido los reemplaza junto con los CG.
AMBER_LINES = {
    "SFW": "¡Hey! Portate bien con el hotel y yo me porto bien contigo.",
    "SUGGESTIVE": "Mmm... ¿otra visita tan pronto? Me estás malacostumbrando.",
    "NSFW": "...",            # stub — Contenido
    "NSFW_NOCTURNO": "...",   # stub — Contenido
}


def make_amber() -> Guest:
    return Guest(name=AMBER_NAME)


def amber_visit_line(affection_value: float) -> str:
    return AMBER_LINES[affection.current_tier(affection_value)]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/Scripts/python.exe -m pytest tests/test_guests.py -q`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add game/velvet/guests.py tests/test_guests.py
git commit -m "feat(engine): Amber como datos (nombre single-source + líneas por tier)"
```

---

### Task 3: Wiring del bridge + panel de objetivos

**Files:**
- Modify: `game/bridge.rpy`
- Modify: `game/reception.rpy` (screen `topbar`)

**Interfaces:**
- Consumes: `velvet.tutorial.advance`, `velvet.tutorial.current_text`, `store.gs`.
- Produces (para las screens): `_objectives_disp` (DynamicDisplayable), `game_tick()` ahora avanza el tutorial y avisa al completar.

- [ ] **Step 1: Importar los módulos nuevos en el bridge**

En `game/bridge.rpy`, dentro de `init python:`, junto a los otros imports:
```python
    import velvet.tutorial
    import velvet.guests
```

- [ ] **Step 2: `game_tick` avanza el tutorial + aviso de fin**

Reemplazar la función `game_tick` en `game/bridge.rpy` por:
```python
    def game_tick():
        # Se llama cada segundo desde el `timer` de las screens activas.
        velvet.session.apply_tick(store.gs, 1.0)
        store.gs.last_seen = time.time()
        if velvet.tutorial.advance(store.gs):
            renpy.notify("Tutorial completado. El hotel ya corre solo.")
```

- [ ] **Step 3: DynamicDisplayable del objetivo actual**

En `game/bridge.rpy`, junto a `_money_disp`/`_income_disp`:
```python
    def _objectives_disp(st, at):
        txt = velvet.tutorial.current_text(store.gs)
        if not txt:
            return Null(), 0.5
        return Text("Objetivo: " + txt, size=28, color="#ffe08a"), 0.5
```

- [ ] **Step 4: Mostrar el objetivo en la topbar**

En `game/reception.rpy`, en `screen topbar()`, agregar tras el `frame` existente (mismo nivel de indentación que `frame:`):
```python
    # Objetivo del tutorial (Null cuando ya está completo -> se oculta solo).
    add DynamicDisplayable(_objectives_disp) xpos 40 ypos 96
```

- [ ] **Step 5: Lint**

Run: `cd /c/Users/fumik/renpy-8.3.7-sdk && ./renpy.exe "C:/Users/fumik/projects/velvet_apartment" lint`
Expected: sin errores.

- [ ] **Step 6: Commit**

```bash
git add game/bridge.rpy game/reception.rpy
git commit -m "feat(ui): tick avanza tutorial + panel de objetivos en topbar"
```

---

### Task 4: Intro VN + siembra de Amber

**Files:**
- Create: `game/intro.rpy`
- Modify: `game/script.rpy` (quitar el `label start` viejo — no puede haber dos)

**Interfaces:**
- Consumes: `velvet.config.STARTING_MONEY`, `velvet.guests.make_amber`, `catch_up_now()`, `store.gs`, `label hub`.
- Produces: `label start`, `define amber`.

- [ ] **Step 1: Vaciar el `start` viejo de `script.rpy`**

Reemplazar TODO el contenido de `game/script.rpy` por (deja de definir `start`; la intro vive en `intro.rpy`):
```python
# Velvet Apartment — el punto de entrada (label start) vive en intro.rpy.
# La navegación del hub se arma en bridge.rpy + reception.rpy.
```

- [ ] **Step 2: Escribir la intro**

`game/intro.rpy`:
```python
# intro.rpy — intro VN (cómica, lineal, voz interna) + siembra de Amber + tutorial.
# Arte = placeholders (scene black); los CG/fondos IA Gen llegan en Contenido.

define amber = Character("Amber", color="#ffb0b0")

label start:
    scene black with fade
    "Tres meses sin empleo. Mi currículum ya daba lástima hasta a mí."
    "Y entonces apareció el anuncio."
    "'Recepcionista nocturno. Sin experiencia. Sueldo: obsceno. Alojamiento incluido.'"
    "Cualquiera con dos dedos de frente habría desconfiado."
    "Yo tenía hambre. Fui."

    scene black
    "La entrevista fue en un edificio que no salía en ningún mapa."
    "El tipo sonreía demasiado. Me ofreció un té."
    "Recuerdo el primer sorbo. Después... nada."
    "..."

    scene black with fade
    "Desperté detrás de un mostrador."
    "Un lobby enorme. Terciopelo por todas partes. Silencio."
    "Sobre el mostrador, un contrato. Firmado. Con mi letra."
    "No recuerdo haberlo firmado."
    "Cláusula única, en negrita: mantener contentas a las huéspedes del hotel."
    "Debería estar aterrado. Pero el sueldo seguía siendo obsceno, así que decidí no hacer preguntas."

    # Siembra del estado narrativo (capital inicial + Amber en la habitación 1).
    $ gs.money = velvet.config.STARTING_MONEY
    $ gs.floors[0].rooms[0].guest = velvet.guests.make_amber()
    $ gs.tutorial_step = 0
    $ gs.tutorial_done = False

    # Presentación de la 1ª huésped.
    "El ascensor sonó. De él bajó una pelirroja con un lazo enorme y demasiada energía."
    amber "¡Holaaa! ¿Tú eres el nuevo? Perfecto, esto estaba MUERTO."
    "La reconocí al instante. No de la vida real. De... otro sitio. Da igual."
    amber "Soy Amber. Habitación uno. Voy a ser tu favorita, ya lo verás."
    amber "Es fácil: te das una vuelta por el Pasillo, me visitas, y con lo que genere el hotel mejoras mi cuarto."
    "Un contrato que no firmé y una huésped que salió de un videojuego. Facilísimo."

    $ catch_up_now()
    jump hub
```
(Sin corchetes/llaves literales en los diálogos → no hay riesgo de interpolación.)

- [ ] **Step 3: Lint**

Run: `cd /c/Users/fumik/renpy-8.3.7-sdk && ./renpy.exe "C:/Users/fumik/projects/velvet_apartment" lint`
Expected: sin errores (un solo `label start`, `amber` definido).

- [ ] **Step 4: Commit**

```bash
git add game/intro.rpy game/script.rpy
git commit -m "feat(narrative): intro VN cómica + siembra de Amber en habitación 1"
```

---

### Task 5: Diálogo de visita por tier (Amber)

**Files:**
- Modify: `game/hallway_room.rpy` (`label hallway_flow`, `screen room`)

**Interfaces:**
- Consumes: `velvet.guests.amber_visit_line`, `velvet.guests.AMBER_NAME`, `do_visit`, `character amber`.
- Produces: `label room_flow(room)`; el botón "Visitar" de Amber devuelve `"visit"`.

- [ ] **Step 1: Extraer `room_flow` y manejar "visit"**

Reemplazar `label hallway_flow:` (líneas 5-12 actuales) en `game/hallway_room.rpy` por:
```python
label hallway_flow:
    while True:
        $ sel = renpy.call_screen("hallway")
        if not isinstance(sel, int) or isinstance(sel, bool):
            return
        call room_flow(gs.floors[current_floor].rooms[sel])


label room_flow(room):
    while True:
        $ res = renpy.call_screen("room", room=room)
        if res == "clicker":
            $ renpy.call_screen("clicker")
        elif res == "visit":
            $ line = velvet.guests.amber_visit_line(room.guest.affection)
            amber "[line]"
            $ do_visit(room.guest)
        else:
            return
```

- [ ] **Step 2: Botón "Visitar" de Amber devuelve "visit"**

En `screen room(room)`, reemplazar la línea:
```python
            textbutton "Visitar (+afecto)" action Function(do_visit, guest) text_size 30
```
por:
```python
            if guest.name == velvet.guests.AMBER_NAME:
                textbutton "Visitar (+afecto)" action Return("visit") text_size 30
            else:
                textbutton "Visitar (+afecto)" action Function(do_visit, guest) text_size 30
```
(Placeholders siguen por el camino rápido `Function` sin restart; Amber muestra su línea vía `room_flow`.)

- [ ] **Step 3: Lint**

Run: `cd /c/Users/fumik/renpy-8.3.7-sdk && ./renpy.exe "C:/Users/fumik/projects/velvet_apartment" lint`
Expected: sin errores.

- [ ] **Step 4: Commit**

```bash
git add game/hallway_room.rpy
git commit -m "feat(narrative): visita a Amber muestra línea por tier (room_flow)"
```

---

### Task 6: Testcase runtime + verificación final

**Files:**
- Modify: `game/testcases.rpy`

**Interfaces:**
- Consumes: todo lo anterior en runtime.

- [ ] **Step 1: Actualizar el testcase `flow`**

En `game/testcases.rpy`, reemplazar el bloque desde la aserción de `reception` hasta antes de `run Quit(...)`. Ahora Amber ya viene sembrada (no se inyecta `TestGuest`), la puerta se llama "Amber", y tras visitar el tutorial avanza. Bloque nuevo (desde `pause 1.5` tras "Despiertas"):
```python
    "Despiertas"
    pause 1.5
    $ assert renpy.get_screen("reception") is not None, "no llegó a recepción"
    $ assert gs.money == velvet.config.STARTING_MONEY, "sin capital inicial"
    # Amber sembrada por la intro (no se inyecta huésped de test).
    $ assert gs.floors[0].rooms[0].guest is not None, "Amber no fue sembrada en la habitación 1"
    $ assert gs.floors[0].rooms[0].guest.name == velvet.guests.AMBER_NAME, "la habitación 1 no tiene a Amber"
    # Tutorial activo en el primer paso.
    $ assert gs.tutorial_done is False, "el tutorial no debería estar completo al arrancar"
    $ assert velvet.tutorial.current_text(gs) == velvet.tutorial.STEPS[0][0], "objetivo inicial incorrecto"
    "MONITOR"
    pause 1.5
    $ assert renpy.get_screen("management") is not None, "MONITOR no abrió gestión"
    "Volver"
    pause 1.5
    "PASILLO"
    pause 1.5
    $ assert renpy.get_screen("hallway") is not None, "PASILLO no abrió el pasillo"
    "Amber"
    pause 1.5
    $ assert renpy.get_screen("room") is not None, "la puerta de Amber no abrió la habitación"
    # Simular la visita (el clic real dispara un say de Amber que el harness no puede cerrar de forma fiable).
    $ do_visit(gs.floors[0].rooms[0].guest)
    $ velvet.tutorial.advance(gs)
    $ assert gs.floors[0].rooms[0].guest.affection > 0, "la visita no subió el afecto"
    $ assert gs.tutorial_step == 1, "el tutorial no avanzó tras la visita"
    "Volver"
    pause 1.5
    $ assert renpy.get_screen("hallway") is not None, "Volver (habitación) no regresó al pasillo"
    "Volver"
    pause 1.5
    $ assert renpy.get_screen("reception") is not None, "Volver del pasillo no regresó a recepción"
    run Quit(confirm=False)
```
(Se conserva la validación del fix `Return(None)->True` y la navegación de retorno.)

- [ ] **Step 2: Lint**

Run: `cd /c/Users/fumik/renpy-8.3.7-sdk && ./renpy.exe "C:/Users/fumik/projects/velvet_apartment" lint`
Expected: sin errores.

- [ ] **Step 3: Runtime test**

Run: `cd /c/Users/fumik/renpy-8.3.7-sdk && ./renpy.exe "C:/Users/fumik/projects/velvet_apartment" test flow`
Expected: exit 0, sin aserciones fallidas.

- [ ] **Step 4: Suite pytest completa**

Run: `./.venv/Scripts/python.exe -m pytest -q`
Expected: PASS (previos + tutorial + guests).

- [ ] **Step 5: Commit**

```bash
git add game/testcases.rpy
git commit -m "test(runtime): flow valida intro/Amber/tutorial + navegación de retorno"
```

- [ ] **Step 6: Actualizar ESTADO.md + memoria**

Actualizar `docs/ESTADO.md` (mover Narrativa de "Restante" a "Hecho", nota de la lección si surge alguna trampa nueva) y la memoria dual (`project_velvet_apartment.md` + memoryClaude). Commit:
```bash
git add docs/ESTADO.md
git commit -m "docs: ESTADO al día — incremento Narrativa hecho"
```

---

## Self-Review

**Spec coverage:**
- Intro VN cómica lineal, voz interna, sin elecciones → Task 4. ✅
- Amber como datos, nombre single-source → Task 2. ✅
- Siembra de Amber en habitación 1 al arrancar → Task 4 (no toca `new_game`). ✅
- Líneas por tier SFW/Suggestive (NSFW/Nocturno stub) → Task 2 (datos) + Task 5 (wiring de visita). ✅
- Tutorial de objetivos con seguimiento (módulo puro + panel + advance en tick) → Tasks 1 y 3. ✅
- Predicate paso 1 = `afecto > 0` → Task 1. ✅
- Tests pytest (advance no salta pasos, marca done, idempotente; siembra de Amber) → Tasks 1, 2, 6. ✅
- Runtime `renpy test flow` extendido → Task 6. ✅
- Trampas Ren'Py (`act()`, `Return("back")`, escapar `[[ ]]`, timer) → Global Constraints + respetadas en Tasks 4/5. ✅
- Misterio como semilla ominosa en clave cómica → Task 4 (contrato firmado/edificio sin mapa). ✅

**Placeholder scan:** sin TBD/TODO; todo el código y los tests están completos.

**Type consistency:** `advance(gs) -> bool`, `current_text(gs) -> str | None`, `STEPS`, `AMBER_NAME`, `make_amber()`, `amber_visit_line(...)` usados idénticos entre tareas. Campos `tutorial_step`/`tutorial_done` definidos en Task 1 y consumidos en 3/4/6 con los mismos nombres. ✅
