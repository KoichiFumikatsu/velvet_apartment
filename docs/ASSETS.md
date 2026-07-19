# Velvet Apartment — Brief de assets (fondos y objetos, SIN personajes)

_Última actualización: 2026-07-18_

Este brief es para generar los **assets que no son de personaje** (fondos, objetos,
props). Los CG de personaje (NSFW) van por el pipeline propio de IA Gen. Estos son
**SFW, sin personas**, así que cualquier generador (Codex/OpenAI images, IA Gen, etc.)
los puede hacer sin fricción.

**Flujo**: generar cada entrada al tamaño indicado → guardar en `game/images/<archivo>`
→ el integrador (Claude) declara las imágenes y reemplaza los `Solid` placeholder por
las imágenes, con lint + `renpy test flow`. No hace falta tocar lógica.

## Ancla de estilo (compartida por TODOS los assets)

Prefijo de estilo a anteponer a cada prompt:

> **Anime visual-novel background art, painterly and detailed. Mysterious, elegant
> boutique hotel at night. Rich velvet textures — deep burgundy and deep purple —
> with warm gold accent lighting and soft rim light. Cinematic, cozy but slightly
> uncanny mood. Cohesive palette: deep purples (#1c1526, #2c2438), warm gold
> (#ffd479), velvet crimson. 16:9, 1920x1080. NO people, NO characters, NO text, NO
> UI, NO logos, NO watermark. Clean empty scene ready for characters/UI to be
> layered on top.**

**Reglas duras** (repetir en negative si el generador lo soporta): sin personas ni
figuras, sin texto ni carteles legibles, sin marcas de agua, sin elementos de UI.
Iluminación y perspectiva **consistentes** entre pantallas (mismo hotel, misma noche).

## Assets — set núcleo

Todos 1920×1080 salvo que se indique. La columna "reemplaza" es el `Solid` placeholder
actual (archivo:línea aprox.).

### 1. `bg_menu_facade.png` — Fachada del hotel de noche (menú principal)
- Reemplaza: `gui.main_menu_background` (`gui.rpy:91`, `Solid("#0a0a1f")`)
- Prompt: _[estilo] Exterior wide shot of a tall, elegant velvet-themed hotel facade
  at night, warm glowing windows, a discreet lit marquee/canopy over the entrance,
  wet cobblestone street reflecting the lights, faint purple mist. Inviting yet
  secretive. Composición con aire arriba/izquierda para el título y botones del menú._

### 2. `bg_game_menu.png` — Interior velvet (menú de guardar/cargar/opciones)
- Reemplaza: `gui.game_menu_background` (`gui.rpy:92`, `Solid("#0f0b16")`)
- Prompt: _[estilo] Dark, out-of-focus interior of a velvet hotel corridor/lounge,
  heavy drapes, low warm lamps, strong vignette. Muy oscuro y de bajo contraste
  (fondo detrás de paneles de UI, no debe competir con el texto)._

### 3. `bg_reception.png` — Recepción, primera persona tras el mostrador
- Reemplaza: `reception.rpy:31` `Solid("#1c1526")`
- Perspectiva: **POV del recepcionista, de pie detrás del mostrador**, mirando el
  lobby. Los objetos deben quedar aproximadamente donde el código pone los hotspots:
  - **Monitor/PC** sobre el mostrador, zona **inferior-derecha** (hotspot xpos1090 ypos560).
  - **Pasillo** (arco/pasaje iluminado) a la **izquierda** (hotspot xpos120 ypos300).
  - **Ascensor** (puertas metálicas art-déco) **centro-izquierda** (hotspot xpos470 ypos340).
  - **Tablón** de anuncios en la pared, zona **superior-central** (hotspot xpos720 ypos170).
  - **Cajón** del mostrador, zona **inferior-derecha bajo el monitor** (hotspot xpos1130 ypos800).
- Prompt: _[estilo] First-person POV standing behind a grand hotel reception desk,
  looking out into a velvet lobby. On the desk to the lower-right: a vintage-styled
  computer monitor. To the left: a warmly lit archway leading to a corridor. Center-
  left: ornate art-deco elevator doors. Upper wall: a cork/notice board. Lower desk:
  a wooden drawer. Balanced, everything readable as a distinct interactive object._

### 4. `bg_hallway.png` — Pasillo con 3 puertas
- Reemplaza: `hallway_room.rpy` `screen hallway` `Solid("#161a24")`
- Nota: el código pone **3 botones** encima (posiciones en un hbox centrado, ~340px
  de ancho cada uno, centro vertical). El fondo debe tener **3 puertas** más o menos
  equiespaciadas a la altura media para que los botones caigan sobre ellas.
- Prompt: _[estilo] A plush velvet hotel corridor seen head-on, three identical
  elegant guest-room doors evenly spaced along the wall, warm sconce lights between
  them, patterned carpet runner receding. Symmetric composition, the three doors
  centered at mid-height._

### 5. `bg_room.png` — Interior de habitación (genérica)
- Reemplaza: `hallway_room.rpy` `screen room` `Solid("#1a1420")`
- Nota: la CG de la huésped se pinta a la **izquierda** (zona xpos120, 620×780). Dejar
  la **mitad izquierda relativamente despejada**; muebles/cama hacia la derecha/fondo.
- Prompt: _[estilo] Cozy velvet hotel guest room interior, a plush bed and drapes to
  the right side, a night window with city glow, warm intimate lighting. Left half of
  the frame kept open/simple (a character will stand there). Inviting, slightly sultry._

### 6. `bg_floors.png` — Ascensor / selector de pisos
- Reemplaza: `floors.rpy:4` `Solid("#12161e")`
- Prompt: _[estilo] Interior of an ornate art-deco elevator cabin, brass floor-panel
  and buttons on one side, polished dark wood and velvet walls, warm downlight.
  Composición con espacio a la izquierda para una lista de pisos (UI)._

### 7. `bg_management.png` — Pantalla del monitor (gestión)
- Reemplaza: `management.rpy:5` `Solid("#101820")` (y el frame interno `#0a0f14`)
- Nota: es la "pantalla del PC". Puede ser un marco de monitor CRT/retro con la
  pantalla oscura (la UI de tabs/tablas se dibuja encima). Bajo contraste.
- Prompt: _[estilo] Close-up of a vintage computer monitor screen glowing faint amber/
  purple, dark desktop UI vibe, subtle scanlines, framed by the dark desk. Screen area
  mostly dark/empty for UI overlay. Retro-management aesthetic._

### 8. `bg_clicker.png` + `obj_package.png` — Minijuego del paquete
- Reemplaza: `clicker.rpy:7` `Solid("#0e0e0e")` (fondo) y el botón "PAQUETE" (`#4d3a2b`)
- `bg_clicker.png` (1920×1080): _[estilo] The reception desk at night, spotlight on a
  mysterious delivery on the counter, motion-blur excitement, focused vignette._
- `obj_package.png` (**PNG transparente**, ~600×400): _[estilo] A single mysterious
  gift package / parcel wrapped in dark paper with a gold ribbon, sitting isolated on
  transparent background, soft rim light. Centered, no shadow bleeding to edges._

### 9. `bg_construccion.png` — Genérico "en construcción" (baja prioridad)
- Reemplaza: `reception.rpy` `screen construccion` `Solid("#14101c")` (tablón/cajón stubs)
- Prompt: _[estilo] A dim velvet storage/back room with covered furniture and a folded
  ladder, "work in progress" feeling but elegant. Muy simple, fondo de un panel de UI._

## Intro (opcional, 2ª tanda)

La intro usa `scene black`. Se puede enriquecer luego con: `bg_ad` (anuncio de empleo),
`bg_interview` (oficina rara), `bg_lobby` (despertar en el lobby — puede **reusar
`bg_reception`**). No es bloqueante; el humor funciona sobre negro.

## Integración (la hace Claude cuando lleguen los PNG)

1. Crear `game/images.rpy` con `image bg_reception = "images/bg_reception.png"` etc.
   (declaración explícita → nombres limpios, independientes del auto-naming).
2. Reemplazar cada `add Solid("#...")` por `add "bg_..."` y los `scene`/`gui.*_background`
   por las imágenes.
3. Hotspots de recepción: botones invisibles (`background None`) + `hover_background`
   translúcido dorado sobre el objeto (highlight programático, sin assets extra).
4. Verificar: `renpy lint` + `renpy test flow` (los PNG deben existir o lint falla por
   imagen no encontrada).
