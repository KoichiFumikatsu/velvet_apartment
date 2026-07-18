# Velvet Apartment — UI Shell (Incremento 1) — Diseño (spec)

- Fecha: 2026-07-18
- Estado: **diseño aprobado** (Bloque A por el usuario; Bloque B decidido en sesión autónoma coherente con lo aprobado).
- Alcance: **Incremento 1** de la UI Ren'Py — shell del hub de recepción + funcionalidad que el motor ya soporta. Inventario/tareas/cámaras/históricos quedan como stubs "en construcción" (incrementos futuros, cada uno con su diseño).
- Consume la API del motor ya mergeado (`game/velvet/`: config, economy, state, affection, actions, hotel, idle, session).
- Resolución **1920×1080 16:9**. Arte = **placeholders programáticos** (Solid/Frame/Text de Ren'Py), cero assets externos; se reemplazan por arte IA Gen sin tocar lógica.

## 1. Modelo de navegación (hub-and-spoke, point-and-click)
- **Recepción** = hub, primera persona detrás del mostrador. Cada objeto es un hotspot (`imagebutton` con `idle`/`hover`; hover sombrea el objeto completo).
- Objeto → destino:
  - **Monitor** (escritorio) → `management` (gestión: habitaciones, huéspedes, fachada; tabs Cámaras/Históricos = stub).
  - **Pasillo** → `hallway` (3 puertas del piso actual; nombre si hay huésped) → `room` (escena de la huésped).
  - **Ascensor** → `floors` (ver pisos, desbloquear/subir).
  - **Tablón de anuncios** → `tasks` (stub "en construcción").
  - **Cajón** (bajo escritorio) → `inventory` (stub "en construcción").
- Navegación por pila de screens; "volver" regresa a recepción. Menú principal = escena aparte (fachada de noche).

## 2. Bridge motor↔Ren'Py
- `default gs = velvet.state.new_game()` en el `store`. Dataclasses del motor son Python puro → **save nativo de Ren'Py los persiste** (pickle).
- Screens **leen** `gs` y renderizan; los botones llaman la API del motor (`velvet.actions.*`, `velvet.hotel.*`) y la screen se refresca en cada interacción. **Ninguna lógica de juego en `.rpy`.**
- Helpers de **display puros y testeables** en `game/velvet/display.py` (sin `import renpy`): formateo de dinero, fracciones de barra, labels de puerta/habitación/costo, nombre visible de tier. Mantiene los `.rpy` finos y da cobertura pytest a la lógica de presentación.

## 3. Tick idle + offline (resuelve la trampa del review del motor)
- `timer 1.0 repeat True` en las screens activas → llama un helper que hace `session.apply_tick(gs, 1.0)` **y** estampa `gs.last_seen = time.time()` (así `last_seen` siempre refleja el último segundo acreditado; evita doble conteo al recargar).
- Al **cargar**/continuar: `session.catch_up(gs, time.time())` acredita el hueco offline (tope 8 h). Se engancha con `after_load` label y al iniciar.
- **Rollback desactivado** (`config.rollback_enabled = False`): choca con dinero en tiempo real.

## 4. Guardado (estilo idle)
- Partida única continua **auto-guardada** (no slots VN). Menú principal = **Continuar / Nueva / Opciones / Salir**.
- Auto-save en puntos clave (al abrir/cerrar sub-pantallas y periódicamente) usando el guardado de Ren'Py.

## 5. Pantallas (Incremento 1)
| Screen | Contenido |
|---|---|
| `main_menu` (reskin) | Fachada del hotel de noche (placeholder: gradiente oscuro + ventanas iluminadas + título "VELVET APARTMENT"). Botones Continuar/Nueva/Opciones/Salir. |
| `reception` | Escena hub 16:9: pared, pasillo, ascensor, escritorio con monitor, cajón, tablón. Cada uno hotspot con hover. Barra superior: dinero + ingreso/s. `timer 1.0`. |
| `management` | Panel del monitor con tabs: **Habitaciones** (lista de habitaciones de pisos desbloqueados: nombre huésped, barra afecto, ingreso/s, botón upgrade), **Fachada** (nivel + botón upgrade), **Huéspedes** (datos), y tabs stub **Cámaras**/**Históricos** ("en construcción"). |
| `hallway` | 3 puertas del piso actual. Puerta ocupada → nombre huésped → `room`. Puerta vacía → "Acondicionar $X" → `condition_room` (paga, llega huésped). |
| `room` | Placeholder de personaje + nombre + barra de afecto + tier actual (SFW/Suggestive/NSFW/Nocturno como texto/panel). Botones: **Visitar** (visit, cooldown), **Servicio** (buy_service), **Mejorar habitación** (upgrade_room). Botón **Paquete** cuando hay evento → `clicker`. |
| `floors` (ascensor) | Lista de pisos; piso actual; "Subir" al siguiente si desbloqueable (`unlock_next_floor`: piso lleno + costo reparación). Pisos bloqueados muestran el requisito. |
| `clicker` | Minijuego de paquete: clicar el paquete durante 15 s; recompensa = `idle.clicker_reward(clicks, income)`; al terminar suma a dinero. Cooldown. |
| `inventory`, `tasks` | Stub "En construcción" + botón volver. Igual las tabs Cámaras/Históricos del monitor. |

## 6. Estrategia de placeholders
- Todo con displayables nativos: `Solid`, `Frame`/borde, `Text`, posicionamiento fijo en 1920×1080. Hotspots = `imagebutton` con `idle`/`hover` construidos de Solid/Text (hover = borde/tinte). Sin PNGs externos.
- Cada hotspot y panel se mapea 1:1 a arte futuro: reemplazar `idle`/`hover` por PNGs (o un `imagemap`) sin tocar la lógica.

## 7. Arquitectura de archivos (game/)
- `game/velvet/` — motor (existe, intacto) + **nuevo** `display.py` (helpers de presentación puros, testeados con pytest).
- `game/script.rpy` — `label start`: init partida / continuar → `reception`. `after_load` → `catch_up`.
- `game/options.rpy` — config (1920×1080, rollback off, nombre, save).
- `game/bridge.rpy` — `default gs`, funciones puente (tick, save helpers) en `init python`.
- `game/screens_*.rpy` — una screen o grupo por archivo (reception, management, hallway_room, floors, clicker, stubs, main_menu). Archivos enfocados, una responsabilidad.

## 8. Verificación (headless)
- `renpy.exe "C:/Users/fumik/projects/velvet_apartment" lint` → debe pasar sin errores (valida sintaxis, refs a screens/labels/estilos).
- `pytest` → los helpers de `display.py` con TDD (más los 34 del motor siguen verdes).
- **Pendiente de humano**: lanzar el juego y validar visualmente/jugando (Ren'Py necesita display; no verificable en esta sesión headless). Se deja anotado en el resumen.

## 9. Fuera de alcance (incrementos futuros, cada uno su diseño)
- **Tareas** diarias/semanales (sistema de quests + recompensas).
- **Inventario** (items, obtención, uso).
- **Datos históricos** (registro + gráficas) y **cámaras**.
- **Contenido**: CG reales por tier + huéspedes como datos (plan de contenido).
- **Narrativa**: intro VN completa (plan de narrativa). En Incremento 1, "Nueva" muestra un stub de 1-2 líneas y entra a recepción.
- Arte real (IA Gen), sonido/música, port Android, prestigio.
