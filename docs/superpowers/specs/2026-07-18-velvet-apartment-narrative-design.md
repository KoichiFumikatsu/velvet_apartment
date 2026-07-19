# Velvet Apartment — Diseño: Incremento Narrativa

- Fecha: 2026-07-18
- Estado: **diseño aprobado**, pendiente plan de implementación.
- Alcance: **Intro VN + 1ª huésped (Amber) como datos + tutorial diegético de objetivos**.
- Reemplaza el stub de 1 línea en `label start` (`game/script.rpy`).

> Ren'Py ya es un motor VN (labels/`say`/`character`/`menu`). Este incremento es
> sobre todo **contenido/escritura** + un rastreador de tutorial chico y puro. No
> introduce sistemas nuevos de arquitectura.

## Decisiones fijas (de este brainstorming)

- **Tono**: cómico / absurdo. Prota resignado; el misterio existe pero nadie lo
  toma muy en serio. Baja fricción hacia el contenido.
- **Protagonista**: voz sarcástica interna, **lineal, sin elecciones**. Sin nombre
  configurable (narrador interno, se refiere a sí mismo en 1ª persona).
- **1ª huésped = Amber**, inspirada en Amber de Genshin. **Riesgo legal aceptado
  conscientemente por Koichi** — contradice la decisión del spec base (evitar
  HoYoverse), registrada como override. Mitigación: el nombre vive en **un solo
  campo de datos** (trivial de cambiar); el arte alterado lo controla Koichi.
- **Tutorial**: objetivos con seguimiento (detecta cada paso hecho y avanza).

## 1. Flujo de arranque (reemplaza `label start`)

Secuencia lineal:

1. **Intro VN** (cutscene, voz interna, cero elecciones). Beats (del spec base §6):
   desempleado desesperado → oferta absurdamente bien pagada (sospechosa) →
   entrevista en lugar raro → se duerme → despierta en el **lobby** → **contrato
   ya firmado** en recepción que no recuerda firmar → deber único: mantener
   satisfechas a las huéspedes.
2. **Siembra de estado narrativo**: capital inicial (`config.STARTING_MONEY`) +
   **Amber ya colocada en habitación 1 (piso 1), ocupada**. (Hoy `new_game`
   arranca con pisos vacíos; la siembra la hace el arranque narrativo, no el motor
   base, para no romper los tests existentes.)
3. **Escena de presentación de Amber** (arquera pelirroja energética; el prota la
   "reconoce"). Arranca el tutorial (`gs.tutorial_step = 0`).
4. `jump hub` → recepción, con el panel de objetivos activo.

El misterio del hotel/contrato queda como **hilo de fondo sembrado** (una o dos
líneas ominosas jugadas en clave cómica); su dosificación por piso es backlog.

## 2. Amber como datos

- Se define **1 huésped concreta como datos**, reemplazando `make_placeholder_guest`
  **solo para la habitación 1**. Las otras 2 huéspedes del piso 1 siguen
  placeholder hasta el incremento de Contenido.
- Campos: `name = "Amber"` (único lugar donde vive el nombre), personalidad/vibe,
  y **líneas por tier** para SFW y Suggestive (saludo, línea de visita). NSFW /
  Nocturno son stubs por ahora (Contenido los llena).
- **Arte = placeholders programáticos** con **nombres de imagen fijos** (p.ej.
  `amber_neutral`, `amber_happy`) declarados como `Text`/`Solid` provisionales.
  Koichi genera los PNG con esos nombres y los dropea sin tocar el script.

## 3. Tutorial de objetivos (`game/velvet/tutorial.py`, puro)

- **Módulo Python puro** (sin `import renpy`, testeable con pytest), coherente con
  la disciplina del motor.
- **Estructura**: lista ordenada de pasos `STEPS = [(texto, predicate(gs)->bool), ...]`.
  `advance(gs)` sube `gs.tutorial_step` mientras el predicate del paso actual dé
  True; al pasar el último paso marca `gs.tutorial_done = True`. Idempotente si ya
  está `done`.
- **Estado en `GameState`**: `tutorial_step: int = 0`, `tutorial_done: bool = False`.
  Picklables → persisten en el save nativo. Se agregan como campos con default
  para no romper saves/tests previos.
- **Pasos** (predicates leen campos ya expuestos por `gs`, sin acoplamiento inverso
  motor→UI):
  1. "Abrí el **Pasillo** y visitá a Amber." → afecto de Amber `> 0` (se siembra en
     0 al arrancar, así que la 1ª visita lo dispara; sin baseline que rastrear).
  2. "Con lo que genera, **mejorá** su habitación." → nivel de la habitación 1 > 1.
  3. "Listo. El hotel gana solo; seguí visitándola para subir su afecto." → cierra
     (`tutorial_done`).
- **UI**: panel de objetivos (placeholder programático, esquina superior), muestra
  `STEPS[gs.tutorial_step]` mientras `not gs.tutorial_done`; se oculta al terminar.
  El hub ya corre `game_tick` cada segundo → ahí se llama `tutorial.advance(gs)`.
  **Cero timers nuevos.**

## 4. Arquitectura y verificación

- **Escritura narrativa**: `.rpy` (labels de intro + escenas de Amber + `character`
  `amber`). **Nada de lógica de juego en `.rpy`** — solo narrativa y `say`.
- **Datos de Amber**: en el motor (`game/velvet/`), junto al resto.
- **Placeholders de arte**: `Text`/`Solid` con nombres de imagen fijos para reemplazo
  directo por PNG.
- **Tests pytest (motor puro)**:
  - `tutorial.advance` avanza con cada predicate cumplido, **no salta pasos**, marca
    `done` tras el último, **idempotente** si ya está `done`.
  - Siembra de Amber: tras el arranque narrativo, la habitación 1 tiene una huésped
    con `name == "Amber"` y el afecto/nivel iniciales correctos.
- **Runtime headless** (`renpy test flow`): extender el testcase — boot → la intro
  corre sin crash → hub → panel de objetivos visible → simular visita → el paso
  avanza y el panel refleja el siguiente objetivo.
- **Trampas Ren'Py que aplican** (de ESTADO.md): mutadores por `act()`;
  `Return("back")` centinela (no `Return(None)`); escapar `[[ ]]` en texto literal;
  `timer 1.0` con `_update_screens=False`.

## 5. Fuera de alcance (backlog, otros incrementos)

- CG NSFW/Nocturno de Amber y arte final (Contenido).
- Huéspedes 2 y 3 del piso 1 como datos reales (Contenido).
- Dosificación completa del misterio por piso (Endgame/Narrativa extendida).
- Elecciones ramificadas / múltiples finales de intro.
