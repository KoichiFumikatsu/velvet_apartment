# bridge.rpy — puente entre el motor puro (game/velvet/) y Ren'Py.
# Ninguna lógica de juego vive aquí: solo estado + llamadas a la API del motor.

init python:
    import time
    import velvet.state
    import velvet.economy
    import velvet.actions
    import velvet.hotel
    import velvet.idle
    import velvet.session
    import velvet.display as vdisplay

    def game_tick():
        # Se llama cada segundo desde el `timer` de las screens activas.
        # Acredita 1s de ingreso y estampa last_seen (evita doble conteo al recargar).
        velvet.session.apply_tick(store.gs, 1.0)
        store.gs.last_seen = time.time()

    def catch_up_now():
        # Acredita el hueco offline (tope 8h) al iniciar/continuar.
        return velvet.session.catch_up(store.gs, time.time())

    def make_placeholder_guest(floor_index, room_index):
        # Huésped placeholder para el shell; el plan de contenido lo reemplaza por datos reales.
        return velvet.state.Guest(name="Huésped %d-%d" % (floor_index + 1, room_index + 1))

    def total_income():
        return velvet.economy.total_income_per_sec(store.gs)

# Estado del juego (persistido por el save nativo de Ren'Py; dataclasses picklables).
default gs = velvet.state.new_game()
default current_floor = 0
default last_clicker = 0.0

# Al cargar una partida: acreditar el tiempo offline.
label after_load:
    $ catch_up_now()
    return
