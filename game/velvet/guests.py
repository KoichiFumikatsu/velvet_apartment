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
