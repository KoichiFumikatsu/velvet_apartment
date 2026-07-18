# AGENTS.md — Velvet Apartment

Contexto que cargan los agentes (**Codex** y **Claude**) al trabajar en este repo. Portable: viaja con el repositorio y es la fuente de verdad del proyecto.

## Qué es
- **Velvet Apartment** — juego **idle** para adultos (+18, hentai) hecho en **Ren'Py**.
- **Estado (2026-07-18): motor de lógica + UI Shell (Incremento 1) HECHOS y jugables.** Ver **`docs/ESTADO.md`** — fuente única de qué está hecho, cómo correrlo/verificarlo, lo restante y las trampas Ren'Py. Diseño en `docs/GDD.md` y `docs/superpowers/specs/`, planes en `docs/superpowers/plans/`.
- **No inventar mecánicas, personajes ni contenido** sin que estén en el GDD/spec. El contenido real (huéspedes, CG, narrativa) es un incremento futuro con su propio diseño.

## Stack
- **Ren'Py 8.3.7** (SDK local en fumihome: `C:\Users\fumik\renpy-8.3.7-sdk`) + Python 3.12.
- **Motor de lógica en `game/velvet/`** (Python puro, sin `import renpy`, testeable con pytest). **UI en `game/*.rpy`** (screens) que solo llama la API del motor. Tunables en `game/velvet/config.py`.
- Verificar: `pytest` (motor) + `renpy lint` + `renpy test flow` (runtime). Detalles en `docs/ESTADO.md`.

## Convenciones de trabajo (para cualquier agente en este repo)
- Idioma: español.
- **Ground-truth**: validar contra el estado real del repo antes de proponer. No inventar archivos, labels ni contenido que no exista. Ante duda, preguntar.
- Flagear de inmediato discrepancias entre lo declarado y lo real.
- **Versionar**: un cambio lógico = un commit, con mensaje descriptivo, en cuanto pase verificación. No commitear código roto.
- Contenido adulto explícito: es intencional (+18). Mantener el contenido dentro del alcance definido en el GDD.
- Comunicación: directa, concisa, sin relleno.

## Núcleo idle (implementado)
Doble recurso: **dinero** pasivo de habitaciones ocupadas (idle/offline) + **afecto** por visitas/servicios que multiplica el ingreso y desbloquea 4 tiers de contenido. Fachada = multiplicador global suave. Pisos de 3 habitaciones + ascensor con muro de reparación. Clicker de paquete acotado. Todo en el motor (`game/velvet/`); ver `docs/superpowers/specs/2026-07-17-velvet-apartment-design.md` y `docs/ESTADO.md`.
