# Velvet Apartment — Estado del proyecto

_Última actualización: 2026-07-18 (incremento Narrativa)_

Juego **idle +18 (hentai)** en **Ren'Py 8.3.7**. Administras un hotel misterioso; las
habitaciones ocupadas generan dinero pasivo, que gastas en upgrades/fachada/expansión;
visitas a las huéspedes suben su afecto, que multiplica ingreso y desbloquea 4 tiers de
contenido. Progresión vertical por pisos. Arte por **IA Gen propio** (placeholders por ahora).

- Local: `C:\Users\fumik\projects\velvet_apartment` (fumihome). Remoto: `git@github.com:KoichiFumikatsu/velvet_apartment.git`.
- Se implementa con **Claude y Codex**. Diseño en `docs/superpowers/specs/`, planes en `docs/superpowers/plans/`.

## Hecho ✅

**Motor de lógica** (`game/velvet/`, Python puro, sin `import renpy`, testeable con pytest):
- `config` (tunables), `economy` (ingreso, costos), `state` (Guest/Room/Floor/GameState), `affection` (tiers), `actions` (visitas/servicios/upgrades), `hotel` (llegada de huésped, muro de piso), `idle` (offline, clicker), `session` (tick, catch_up), `display` (helpers de presentación).
- **42 tests pytest** verdes.

**UI Shell (Incremento 1)** (`game/*.rpy`, Ren'Py):
- Hub de recepción en 1ª persona (16:9) con objetos interactuables (hover). **Funcionales**: Monitor→gestión (habitaciones/fachada/huéspedes), Pasillo→puertas→habitación (visitar/servicio/mejorar), Ascensor→pisos (desbloquear/subir), clicker de paquete. **Stubs "en construcción"**: Cajón/Inventario, Tablón/Tareas, tabs Cámaras/Históricos.
- Menú principal (fachada oscura), guardado + offline `catch_up`, tick de ingreso optimizado, capital inicial ($50) para arrancar.
- Arte = **placeholders programáticos** (Solid/Frame/Text); se reemplazan por arte IA Gen sin tocar lógica.
- Testcase runtime `flow` (headless) verde.

**Narrativa (Incremento)** (`game/intro.rpy`, `game/velvet/{tutorial,guests}.py`):
- **Intro VN** cómica lineal (voz interna sarcástica, sin elecciones): desempleado → oferta sospechosa → despierta en el lobby → contrato ya firmado. Reemplaza el stub de 1 línea en `label start` (ahora en `intro.rpy`; `script.rpy` quedó como puntero).
- **Amber** = 1ª huésped, sembrada en la habitación 1 al arrancar, definida como **datos** (`velvet/guests.py`, nombre single-source en `AMBER_NAME`, líneas de visita por tier SFW/Suggestive; NSFW/Nocturno stub). Inspirada en Amber de Genshin — **riesgo legal HoYoverse aceptado conscientemente** (override del spec base; nombre en un solo campo para cambiarlo fácil). La visita a Amber muestra su línea por tier (`room_flow`); las otras huéspedes siguen placeholder.
- **Tutorial de objetivos** (`velvet/tutorial.py`, puro): panel en la topbar que detecta pasos (visitar Amber → mejorar su habitación) y avanza en el `game_tick`; aviso `notify` al completar. `gs.tutorial_step`/`tutorial_done` persisten en el save.
- **Verificación**: pytest 50/50; runtime `test flow` extendido (avanza la intro completa con `click until "MONITOR"`, valida siembra de Amber + tutorial activo + **visita real** que ejerce la interpolación `[line]` + navegación de retorno). Control negativo confirmó que el harness ejecuta los asserts.

## Cómo correr / verificar

- **Jugar**: `& "C:\Users\fumik\renpy-8.3.7-sdk\renpy.exe" "C:\Users\fumik\projects\velvet_apartment"` → menú → **Nueva** (el capital inicial solo aplica a partida nueva).
- **Tests motor+display+flujo**: `.\.venv\Scripts\python.exe -m pytest -v` (50 tests)
- **Lint Ren'Py**: `cd C:\Users\fumik\renpy-8.3.7-sdk; .\renpy.exe "C:\Users\fumik\projects\velvet_apartment" lint`
- **Test runtime headless**: `.\renpy.exe "C:\Users\fumik\projects\velvet_apartment" test flow` (exit 0 = ok)

## Restante — incrementos (cada uno con su diseño → plan → implementación)

1. **Contenido**: resto de huéspedes reales como **datos** (Amber ya hecha; faltan las 2 del piso 1, reemplazar `make_placeholder_guest`) + CG por tier (SFW/Suggestive/NSFW/Nocturno) + arte del hub/habitaciones/Amber (IA Gen — Koichi genera los PNG con nombres fijos). Evento paquete con arte.
2. ~~**Narrativa**: intro VN + 1ª huésped tutorial~~ **HECHO 2026-07-18** (ver arriba). Pendiente ampliación: dosificación del misterio por piso, elecciones/múltiples finales.
3. **Tareas** (tablón): sistema de tareas diarias/semanales + recompensas. Reemplaza el stub `construccion`.
4. **Inventario** (cajón): items, obtención, uso. Reemplaza stub.
5. **Históricos + Cámaras** (tabs del monitor): registro/gráficas + ver estado en vivo. Reemplazan stubs.
6. **Endgame / pulido**: prestigio/reputación, pisos 2+ con arte, balance fino de curvas, sonido/música, port Android.

## Decisiones fijas y trampas Ren'Py (críticas)

- **Elenco "inspirado en"** legalmente distinto (fan-art); evitar franquicias agresivas (HoYoverse/Genshin, etc.).
- Motor puro (sin `import renpy`); **todos los tunables en `config.py`**.
- **`Return(None)` fuera del menú devuelve `True`, no `None`** → usar centinela explícito (`Return("back")`) cuando el valor de `call_screen` se usa como índice/condición.
- **Texto con `[...]` literal se interpreta como interpolación** → escapar (`[[ ]]`) o evitar corchetes.
- **Acciones que llaman funciones del motor que devuelven bool** deben ir por el wrapper `act()` (en `bridge.rpy`), o el retorno no-None cierra la interacción de la screen.
- **Tick idle**: `timer 1.0 action Function(game_tick, _update_screens=False)` + dinero/ingreso vía `DynamicDisplayable` (redibujo sin reiniciar la interacción).
- Verificación de `.rpy` headless: `renpy lint` + framework `renpy test` con `assert renpy.get_screen(...)`.
- **`renpy test`: `click until "<pattern>"`** avanza diálogo (click ciego repetido) hasta que aparece un botón focusable que matchea el patrón, y entonces lo clickea — forma robusta de saltar una intro VN larga hasta el hub sin overshoot (el `until` cambia al target apenas está `ready()`, antes de otro click ciego). `Pattern.ready()` solo matchea **focusables** (botones), no `Text` sueltos.
- **El exit code de `renpy test` se enmascara si se pipea** (`... | tail` devuelve el exit de `tail`). Capturar a archivo y leer `$?` directo; un assert fallido escribe `traceback.txt` y sale ≠0.
