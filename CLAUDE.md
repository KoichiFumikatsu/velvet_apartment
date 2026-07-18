# CLAUDE.md — Velvet Apartment

Juego **idle +18 (hentai) en Ren'Py**, implementado con **Claude y Codex**. El contexto del proyecto (qué es, stack, convenciones) vive en [AGENTS.md](AGENTS.md) — **leerlo primero**; es la fuente de verdad portable. El diseño se cierra en [docs/GDD.md](docs/GDD.md) antes de implementar.

## Local (fumihome)
- Ruta: `C:\Users\fumik\projects\velvet_apartment`
- Remoto: `git@github.com:KoichiFumikatsu/velvet_apartment.git` (SSH, conectado). Carpeta local y repo coinciden en nombre (`velvet_apartment`, guion bajo).
- Ren'Py SDK: `C:\Users\fumik\renpy-8.3.7-sdk`
- Correr (cuando exista `game/`): `& "C:\Users\fumik\renpy-8.3.7-sdk\renpy.exe" "C:\Users\fumik\projects\velvet_apartment"`
  - Trampa conocida del launcher `renpy.exe` en fumihome: ver memoria `project_tlgames_fumihome_port.md` (cwd del launcher).

## Persistencia de memoria (dual)
- memoryClaude: `memory/velvet-apartment.md` (indexada en el `CLAUDE.md` del repo memoryClaude)
- auto-memory: `~/.claude/projects/C--/memory/project_velvet_apartment.md` (indexada en `MEMORY.md`)
Guardar solo lo **no obvio** y **reutilizable**. El estado vivo y las convenciones del proyecto van en `AGENTS.md` (viaja con el repo); el diseño en `docs/GDD.md`.

## Estado
Diseño desde cero. **No hacer scaffolding de `game/` ni implementar mecánicas hasta cerrar el concepto base en `docs/GDD.md`** (brainstorming pendiente).
