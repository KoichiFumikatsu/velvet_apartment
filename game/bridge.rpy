# bridge.rpy — puente entre el motor puro (game/velvet/) y Ren'Py.
# Ninguna lógica de juego vive aquí: solo estado + llamadas a la API del motor.

init python:
    import time
    import velvet.state
    import velvet.config
    import velvet.economy
    import velvet.actions
    import velvet.hotel
    import velvet.idle
    import velvet.session
    import velvet.tutorial
    import velvet.guests
    import velvet.display as vdisplay

    def game_tick():
        # Se llama cada segundo desde el `timer` de las screens activas.
        # Acredita 1s de ingreso y estampa last_seen (evita doble conteo al recargar).
        velvet.session.apply_tick(store.gs, 1.0)
        store.gs.last_seen = time.time()
        if velvet.tutorial.advance(store.gs):
            renpy.notify("Tutorial completado. El hotel ya corre solo.")

    def catch_up_now():
        # Acredita el hueco offline (tope 8h) al iniciar/continuar.
        return velvet.session.catch_up(store.gs, time.time())

    def make_placeholder_guest(floor_index, room_index):
        # Huésped placeholder para el shell; el plan de contenido lo reemplaza por datos reales.
        return velvet.state.Guest(name="Huésped %d-%d" % (floor_index + 1, room_index + 1))

    def total_income():
        return velvet.economy.total_income_per_sec(store.gs)

    def act(fn, *args, **kwargs):
        # Ejecuta una acción del motor y DESCARTA su bool de retorno.
        # Si no se descarta, el valor no-None cierra la interacción de la screen
        # (semántica de Function en Ren'Py) y expulsa/corrompe la navegación.
        fn(*args, **kwargs)

    def do_visit(guest):
        # Visita con cooldown real (lee el reloj al hacer clic). Sin retorno (ver act()).
        velvet.actions.visit(guest, time.time())

    def package_ready():
        return (time.time() - store.last_clicker) >= velvet.config.CLICKER_COOLDOWN_SEC

    def start_package_cooldown():
        store.last_clicker = time.time()

    def finish_clicker(clicks, income):
        reward = velvet.idle.clicker_reward(clicks, income)
        store.gs.money += reward
        start_package_cooldown()
        renpy.notify("Paquete: +%s" % vdisplay.format_money(reward))
        return reward

    # DynamicDisplayables: se redibujan solos (sin reiniciar la interacción),
    # así el dinero/ingreso se ven en vivo aunque el tick use _update_screens=False.
    def _money_disp(st, at):
        return Text(vdisplay.format_money(store.gs.money), size=44, color="#ffd479"), 0.25

    def _income_disp(st, at):
        return Text(vdisplay.room_income_label(total_income()), size=30, color="#c9b8e0"), 0.5

    def _objectives_disp(st, at):
        txt = velvet.tutorial.current_text(store.gs)
        if not txt:
            return Null(), 0.5
        return Text("Objetivo: " + txt, size=28, color="#ffe08a"), 0.5

# Estado del juego (persistido por el save nativo de Ren'Py; dataclasses picklables).
default gs = velvet.state.new_game()
default current_floor = 0
default last_clicker = 0.0

# Al cargar una partida: acreditar el tiempo offline.
label after_load:
    $ catch_up_now()
    return
