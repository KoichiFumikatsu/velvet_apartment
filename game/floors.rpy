# floors.rpy — ascensor: navegar entre pisos y desbloquear el siguiente.

screen floors():
    add Solid("#12161e")
    text "Ascensor — Pisos" size 40 color "#ffd479" xpos 60 ypos 90

    vbox:
        xpos 60 ypos 180 spacing 16

        for fi, floor in enumerate(gs.floors):
            if floor.unlocked:
                hbox:
                    spacing 24 yalign 0.5
                    text "Piso %d" % (fi + 1) size 30 xsize 200
                    if fi == current_floor:
                        text "(actual)" size 24 color "#8fd18f" xsize 160
                    else:
                        textbutton "Ir a este piso" action SetVariable("current_floor", fi) text_size 24

        null height 30

        $ top = gs.floors[-1]
        $ full = velvet.hotel.floor_full(top)
        $ rcost = velvet.hotel.repair_cost(top.index)
        if full:
            textbutton "Reparar y subir al siguiente piso (%s)" % vdisplay.cost_label(rcost):
                action Function(act, velvet.hotel.unlock_next_floor, gs, top)
                sensitive gs.money >= rcost
                text_size 30
        else:
            text "Para subir: llena las 3 habitaciones del piso %d y paga la reparación (%s)." % (top.index + 1, vdisplay.cost_label(rcost)) size 26 color "#c9b8e0"

    textbutton "Volver" action Return() xpos 60 ypos 940 text_size 30
    use topbar
    timer 1.0 action Function(game_tick, _update_screens=False) repeat True
