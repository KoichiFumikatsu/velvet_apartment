# Testcase automatizado del flujo del shell (solo modo desarrollo).
# Correr: renpy.exe "<proyecto>" test flow
#
# Valida: boot -> intro VN completa (cada say renderiza sin crash de
# interpolación) -> recepción -> Amber sembrada + tutorial activo -> navegación
# monitor/pasillo/habitación -> visita REAL (say por tier de Amber, valida
# interpolación [line]) -> tutorial avanza -> navegación de retorno (fix
# Return(None)->True: el Volver del pasillo va a recepción, no rebota).

testcase flow:
    "Start"
    pause 1.0
    # Avanza línea por línea hasta que aparece la recepción, luego abre el Monitor.
    click until "MONITOR"
    pause 1.0
    $ assert renpy.get_screen("management") is not None, "MONITOR no abrió gestión tras la intro"
    # Amber sembrada por la intro + tutorial activo en el primer paso.
    $ assert gs.floors[0].rooms[0].guest is not None, "Amber no fue sembrada en la habitación 1"
    $ assert gs.floors[0].rooms[0].guest.name == velvet.guests.AMBER_NAME, "la habitación 1 no tiene a Amber"
    $ assert gs.tutorial_done is False, "el tutorial no debería estar completo al arrancar"
    $ assert velvet.tutorial.current_text(gs) == velvet.tutorial.STEPS[0][0], "objetivo inicial incorrecto"
    "Volver"
    pause 1.0
    $ assert renpy.get_screen("reception") is not None, "Volver del Monitor no regresó a recepción"
    "PASILLO"
    pause 1.0
    $ assert renpy.get_screen("hallway") is not None, "PASILLO no abrió el pasillo"
    "Amber"
    pause 1.0
    $ assert renpy.get_screen("room") is not None, "la puerta de Amber no abrió la habitación"
    # Visita REAL: dispara el say por tier de Amber (valida interpolación [line] en runtime).
    "Visitar"
    pause 0.5
    click
    pause 1.0
    $ assert renpy.get_screen("room") is not None, "tras la visita la habitación no volvió a abrir"
    $ assert gs.floors[0].rooms[0].guest.affection > 0, "la visita no subió el afecto"
    $ velvet.tutorial.advance(gs)
    $ assert gs.tutorial_step == 1, "el tutorial no avanzó tras la visita"
    "Volver"
    pause 1.0
    $ assert renpy.get_screen("hallway") is not None, "Volver (habitación) no regresó al pasillo"
    "Volver"
    pause 1.0
    $ assert renpy.get_screen("reception") is not None, "Volver del pasillo no regresó a recepción"
    run Quit(confirm=False)
