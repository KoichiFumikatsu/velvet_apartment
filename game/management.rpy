# management.rpy — pantalla del monitor (gestión del hotel).

screen management():
    default tab = "rooms"
    add Solid("#101820")

    vbox:
        xpos 60 ypos 90 spacing 20

        # Tabs
        hbox:
            spacing 12
            textbutton "Habitaciones" action SetScreenVariable("tab", "rooms") text_size 26
            textbutton "Fachada" action SetScreenVariable("tab", "facade") text_size 26
            textbutton "Huéspedes" action SetScreenVariable("tab", "guests") text_size 26
            textbutton "Cámaras" action SetScreenVariable("tab", "cameras") text_size 26
            textbutton "Históricos" action SetScreenVariable("tab", "history") text_size 26

        frame:
            xsize 1800 ysize 820
            background Solid("#0a0f14")
            padding (30, 24)

            if tab == "rooms":
                use mgmt_rooms
            elif tab == "facade":
                use mgmt_facade
            elif tab == "guests":
                use mgmt_guests
            else:
                vbox:
                    spacing 20
                    text "En construcción" size 40 color "#ffd479"
                    text "Cámaras y datos históricos llegan en un próximo incremento." size 26 color "#c9b8e0"

    textbutton "Volver" action Return() xpos 60 ypos 940 text_size 30
    use topbar
    timer 1.0 action Function(game_tick, _update_screens=False) repeat True


screen mgmt_rooms():
    viewport:
        scrollbars "vertical" mousewheel True
        vbox:
            spacing 10
            for fi, floor in enumerate(gs.floors):
                if floor.unlocked:
                    text "Piso %d" % (fi + 1) size 30 color "#ffd479"
                    for ri, room in enumerate(floor.rooms):
                        $ dlabel = vdisplay.door_label(room)
                        $ up_cost = velvet.economy.room_upgrade_cost(room.upgrade_level)
                        $ rincome = velvet.economy.room_income(room, gs.facade_level, fi)
                        hbox:
                            spacing 24 yalign 0.5
                            text "H%d: %s" % (ri + 1, dlabel) size 26 xsize 320
                            text "Nvl %d" % room.upgrade_level size 24 xsize 110 color "#c9b8e0"
                            if room.occupied:
                                bar value StaticValue(room.guest.affection, 100) xsize 240 ysize 22 yalign 0.5
                                text vdisplay.tier_display(room.guest) size 22 xsize 200 color "#e0a0c0"
                            else:
                                text "—" size 24 xsize 440 color "#666666"
                            text vdisplay.room_income_label(rincome) size 24 xsize 150 color "#8fd18f"
                            textbutton "Mejorar (%s)" % vdisplay.cost_label(up_cost):
                                action Function(act, velvet.actions.upgrade_room, gs, room)
                                sensitive gs.money >= up_cost
                                text_size 22


screen mgmt_facade():
    $ fcost = velvet.economy.facade_cost(gs.facade_level)
    vbox:
        spacing 24
        text "Fachada del hotel" size 40 color "#ffd479"
        text "Nivel actual: %d  (+%d%% al ingreso global)" % (gs.facade_level, int(gs.facade_level * 10)) size 28
        text "Cada nivel suma +10%% al ingreso de todas las habitaciones." size 24 color "#c9b8e0"
        textbutton "Mejorar fachada (%s)" % vdisplay.cost_label(fcost):
            action Function(act, velvet.actions.upgrade_facade, gs)
            sensitive gs.money >= fcost
            text_size 28


screen mgmt_guests():
    viewport:
        scrollbars "vertical" mousewheel True
        vbox:
            spacing 12
            text "Huéspedes" size 40 color "#ffd479"
            for fi, floor in enumerate(gs.floors):
                for room in floor.rooms:
                    if room.occupied:
                        hbox:
                            spacing 24 yalign 0.5
                            text room.guest.name size 26 xsize 320
                            bar value StaticValue(room.guest.affection, 100) xsize 300 ysize 22 yalign 0.5
                            text "Afecto %d — %s" % (int(room.guest.affection), vdisplay.tier_display(room.guest)) size 24 color "#e0a0c0"
