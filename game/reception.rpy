# reception.rpy — hub de recepción (hub-and-spoke) + navegación.

label hub:
    $ dest = renpy.call_screen("reception")
    if dest == "management":
        $ renpy.call_screen("management")
    elif dest == "hallway":
        call hallway_flow
    elif dest == "floors":
        $ renpy.call_screen("floors")
    elif dest == "tasks":
        $ renpy.call_screen("construccion", titulo="Tablón de anuncios — Tareas")
    elif dest == "inventory":
        $ renpy.call_screen("construccion", titulo="Cajón — Inventario")
    jump hub


# Barra superior reutilizable: dinero + ingreso/s (DynamicDisplayable = live sin restart).
screen topbar():
    frame:
        xfill True ypos 0
        background Solid("#00000099")
        padding (30, 14)
        hbox:
            spacing 40
            add DynamicDisplayable(_money_disp)
            add DynamicDisplayable(_income_disp) yalign 1.0


screen reception():
    add Solid("#1c1526")

    # Objetos interactuables (placeholders: bloque + hover; con arte pasan a idle/hover PNGs).
    textbutton "PASILLO" action Return("hallway"):
        xpos 120 ypos 300 xsize 300 ysize 420
        text_xalign 0.5 text_yalign 0.5 text_size 30
        background "#2b3a4d" hover_background "#4a6a8d"
    textbutton "ASCENSOR" action Return("floors"):
        xpos 470 ypos 340 xsize 180 ysize 380
        text_xalign 0.5 text_yalign 0.5 text_size 26
        background "#3a2b4d" hover_background "#5a4b7d"
    textbutton "TABLÓN" action Return("tasks"):
        xpos 720 ypos 170 xsize 240 ysize 170
        text_xalign 0.5 text_yalign 0.5 text_size 26
        background "#4d3a2b" hover_background "#7d5a3b"
    textbutton "MONITOR" action Return("management"):
        xpos 1090 ypos 560 xsize 380 ysize 210
        text_xalign 0.5 text_yalign 0.5 text_size 32
        background "#22333b" hover_background "#3a5a6b"
    textbutton "CAJÓN" action Return("inventory"):
        xpos 1130 ypos 800 xsize 300 ysize 120
        text_xalign 0.5 text_yalign 0.5 text_size 24
        background "#2b2b2b" hover_background "#4a4a4a"

    use topbar
    timer 1.0 action Function(game_tick, _update_screens=False) repeat True


# Panel genérico "en construcción" (tablón/inventario/tabs stub).
screen construccion(titulo="En construcción"):
    add Solid("#14101c")
    frame:
        align (0.5, 0.5) padding (80, 60)
        vbox:
            spacing 30
            text titulo size 46 color "#ffd479" xalign 0.5
            text "En construcción — llega en un próximo incremento." size 28 color "#c9b8e0" xalign 0.5
            textbutton "Volver" action Return() xalign 0.5 text_size 30
    use topbar
    timer 1.0 action Function(game_tick, _update_screens=False) repeat True
