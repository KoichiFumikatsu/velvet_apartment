# hallway_room.rpy — pasillo (3 puertas del piso actual) y escena de habitación.

label hallway_flow:
    while True:
        $ sel = renpy.call_screen("hallway")
        if sel is None:
            return
        $ res = renpy.call_screen("room", room=gs.floors[current_floor].rooms[sel])
        if res == "clicker":
            $ renpy.call_screen("clicker")


screen hallway():
    $ floor = gs.floors[current_floor]
    add Solid("#161a24")
    text "Piso %d — Pasillo" % (current_floor + 1) size 40 color "#ffd479" xpos 60 ypos 90

    hbox:
        align (0.5, 0.5) spacing 60
        for ri, room in enumerate(floor.rooms):
            if room.occupied:
                textbutton room.guest.name action Return(ri):
                    xsize 340 ysize 520 text_xalign 0.5 text_yalign 0.5 text_size 30
                    background "#3a2f4d" hover_background "#5a4f7d"
            else:
                $ ccost = velvet.hotel.condition_cost(current_floor)
                textbutton "Puerta vacía\nAcondicionar\n%s" % vdisplay.cost_label(ccost):
                    action Function(velvet.hotel.condition_room, gs, floor, room, make_placeholder_guest(current_floor, ri))
                    sensitive gs.money >= ccost
                    xsize 340 ysize 520 text_xalign 0.5 text_yalign 0.5 text_size 26
                    background "#242430" hover_background "#3a3a4a"

    textbutton "Volver" action Return(None) xpos 60 ypos 940 text_size 30
    use topbar
    timer 1.0 action Function(game_tick) repeat True


screen room(room):
    $ guest = room.guest
    $ scost = velvet.actions.service_cost(guest.services_bought)
    $ ucost = velvet.economy.room_upgrade_cost(room.upgrade_level)
    add Solid("#1a1420")

    # Placeholder del personaje.
    frame:
        xpos 120 ypos 140 xsize 620 ysize 780
        background Solid("#2c2438")
        vbox:
            align (0.5, 0.5) spacing 16
            text guest.name size 44 color "#ffd479" xalign 0.5
            text "[ arte de la huésped ]" size 24 color "#7a6a8a" xalign 0.5

    # Panel de interacción.
    vbox:
        xpos 820 ypos 180 spacing 22
        text "Afecto: %d / 100" % int(guest.affection) size 30
        bar value StaticValue(guest.affection, 100) xsize 520 ysize 28
        text "Contenido: %s" % vdisplay.tier_display(guest) size 28 color "#e0a0c0"
        null height 20
        textbutton "Visitar (+afecto)" action Function(do_visit, guest) text_size 30
        textbutton "Servicio (%s, +afecto)" % vdisplay.cost_label(scost):
            action Function(velvet.actions.buy_service, gs, guest)
            sensitive gs.money >= scost
            text_size 30
        textbutton "Mejorar habitación (%s)" % vdisplay.cost_label(ucost):
            action Function(velvet.actions.upgrade_room, gs, room)
            sensitive gs.money >= ucost
            text_size 30
        textbutton "Recibir paquete (clicker)" action Return("clicker") sensitive package_ready() text_size 30
        null height 20
        textbutton "Volver" action Return(None) text_size 30

    use topbar
    timer 1.0 action Function(game_tick) repeat True
