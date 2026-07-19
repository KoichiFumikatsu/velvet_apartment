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
