# Velvet Apartment — Estado del proyecto

_Última actualización: 2026-07-18_

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

## Cómo correr / verificar

- **Jugar**: `& "C:\Users\fumik\renpy-8.3.7-sdk\renpy.exe" "C:\Users\fumik\projects\velvet_apartment"` → menú → **Nueva** (el capital inicial solo aplica a partida nueva).
- **Tests motor+display+flujo**: `.\.venv\Scripts\python.exe -m pytest -v`
- **Lint Ren'Py**: `cd C:\Users\fumik\renpy-8.3.7-sdk; .\renpy.exe "C:\Users\fumik\projects\velvet_apartment" lint`
- **Test runtime headless**: `.\renpy.exe "C:\Users\fumik\projects\velvet_apartment" test flow` (exit 0 = ok)

## Restante — incrementos (cada uno con su diseño → plan → implementación)

1. **Contenido**: huéspedes reales como **datos** (reemplazar `make_placeholder_guest`) + CG por tier (SFW/Suggestive/NSFW/Nocturno) + arte del hub/habitaciones (IA Gen). Evento paquete con arte.
2. **Narrativa**: intro VN completa (desempleado → entrevista sospechosa → despertar en el lobby → contrato firmado → 1ª huésped tutorial, "inspirada en"). Reemplaza el stub de 1 línea en `start`.
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
