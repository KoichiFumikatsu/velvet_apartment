# clicker.rpy — minijuego de paquete. Clic rápido durante la sesión; recompensa acotada.

screen clicker():
    default clicks = 0
    default remaining = velvet.config.CLICKER_SESSION_SEC
    $ income = total_income()
    add Solid("#0e0e0e")

    vbox:
        align (0.5, 0.5) spacing 30
        text "¡Paquete! Haz clic rápido" size 44 color "#ffd479" xalign 0.5
        text "Tiempo: %d s" % int(remaining) size 32 xalign 0.5
        text "Clics: %d" % clicks size 30 color "#8fd18f" xalign 0.5
        textbutton "PAQUETE":
            action SetScreenVariable("clicks", clicks + 1)
            xsize 420 ysize 260 text_xalign 0.5 text_yalign 0.5 text_size 48
            background "#4d3a2b" hover_background "#7d5a3b"
            xalign 0.5

    # Cuenta regresiva de la sesión.
    timer 1.0 repeat True:
        action If(remaining > 1.5,
                  SetScreenVariable("remaining", remaining - 1),
                  [Function(finish_clicker, clicks, income), Return()])

    # Tick de ingreso idle (coherente con las demás screens; no se pierde ingreso durante el clicker).
    timer 1.0 action Function(game_tick) repeat True
