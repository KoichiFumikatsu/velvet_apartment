# AGENTS.md — Velvet Apartment

Contexto que cargan los agentes (**Codex** y **Claude**) al trabajar en este repo. Portable: viaja con el repositorio y es la fuente de verdad del proyecto.

## Qué es
- **Velvet Apartment** — juego **idle** para adultos (+18, hentai) hecho en **Ren'Py**.
- Estado: **diseño desde cero** (2026-07-17). No existía documentación previa: se buscó en fumihome, FumiWork, koilinux y Google Drive y no había nada — se arranca en blanco.
- El diseño se define en `docs/GDD.md` mediante brainstorming antes de implementar. **No inventar mecánicas, personajes ni contenido sin que estén en el GDD.**

## Stack
- **Ren'Py 8.3.7** (SDK local en fumihome: `C:\Users\fumik\renpy-8.3.7-sdk`). Lenguaje: Ren'Py script + Python.
- Aún sin árbol `game/` — se genera cuando el concepto base del GDD esté cerrado.

## Convenciones de trabajo (para cualquier agente en este repo)
- Idioma: español.
- **Ground-truth**: validar contra el estado real del repo antes de proponer. No inventar archivos, labels ni contenido que no exista. Ante duda, preguntar.
- Flagear de inmediato discrepancias entre lo declarado y lo real.
- **Versionar**: un cambio lógico = un commit, con mensaje descriptivo, en cuanto pase verificación. No commitear código roto.
- Contenido adulto explícito: es intencional (+18). Mantener el contenido dentro del alcance definido en el GDD.
- Comunicación: directa, concisa, sin relleno.

## Núcleo idle (a definir en GDD)
Un juego idle vive de su bucle de progreso pasivo: qué recurso se acumula sin intervención, qué mejoras lo aceleran, y qué desbloquea contenido. Todo eso se cierra en `docs/GDD.md` antes de tocar Ren'Py.
