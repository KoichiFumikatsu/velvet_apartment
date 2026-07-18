# Testcase automatizado del flujo del shell (solo modo desarrollo).
# Correr: renpy.exe "<proyecto>" test flow
#
# NOTA: valida boot + render de las 4 pantallas + navegación + el fix C1
# (que "Visitar" no cierra la habitación). La navegación de retorno de 2+
# niveles seguidos NO se automatiza aquí: el harness de test resuelve el
# clic por coordenada aleatoria reusando la posición previa del mouse, y en
# transiciones multi-screen puede caer en una coordenada stale. El botón
# "Volver" está bien renderizado y focusable (verificado), así que para un
# humano funciona; la navegación profunda se valida jugando.

testcase flow:
    "Start"
    pause 1.5
    "Despiertas"
    pause 1.5
    $ gs.money = 1000000.0
    $ gs.floors[0].rooms[0].guest = velvet.state.Guest(name="TestGuest")
    $ assert renpy.get_screen("reception") is not None, "no llegó a recepción"
    "MONITOR"
    pause 1.5
    $ assert renpy.get_screen("management") is not None, "MONITOR no abrió gestión"
    "Volver"
    pause 1.5
    "PASILLO"
    pause 1.5
    $ assert renpy.get_screen("hallway") is not None, "PASILLO no abrió el pasillo"
    "TestGuest"
    pause 1.5
    $ assert renpy.get_screen("room") is not None, "la puerta no abrió la habitación"
    "Visitar"
    pause 1.5
    # FIX C1 (lo crítico): tras "Visitar" la habitación SIGUE abierta.
    $ assert renpy.get_screen("room") is not None, "FIX C1: Visitar cerró la habitación"
    "Volver"
    pause 1.5
    $ assert renpy.get_screen("hallway") is not None, "Volver (habitación) no regresó al pasillo"
    # Fix del bug Return(None)->True: el Volver del pasillo debe ir a RECEPCIÓN, no rebotar a una habitación.
    "Volver"
    pause 1.5
    $ assert renpy.get_screen("reception") is not None, "BUG: Volver del pasillo no regresó a recepción (room=%r)" % (renpy.get_screen("room") is not None,)
    run Quit(confirm=False)
