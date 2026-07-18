"""Integración: simula la secuencia de llamadas que hacen las screens del shell,
para validar el flujo de juego completo a nivel de lógica (sin runtime Ren'Py)."""

from velvet import actions, affection, config, economy, hotel, idle, session, state


def test_full_play_flow():
    gs = state.new_game()
    floor = gs.floors[0]
    gs.money = 5000.0

    # Pasillo: acondicionar las 3 puertas -> llegan huéspedes (como el botón "Acondicionar").
    for ri, room in enumerate(floor.rooms):
        assert hotel.condition_room(gs, floor, room, state.Guest(name="H1-%d" % (ri + 1))) is True
        assert room.occupied
    assert hotel.floor_full(floor) is True
    assert economy.total_income_per_sec(gs) > 0

    # Habitación: visitar repetidamente (avanzando el reloj más allá del cooldown) sube de tier.
    g = floor.rooms[0].guest
    assert affection.current_tier(g.affection) == "SFW"
    t = 0.0
    for _ in range(30):
        t += config.VISIT_COOLDOWN_SEC
        actions.visit(g, t)
    assert g.affection == 100.0
    assert affection.current_tier(g.affection) == "NSFW_NOCTURNO"

    # Servicio pagado sube afecto (aquí ya está al tope, pero la compra debe proceder y cobrar).
    money_before = gs.money
    assert actions.buy_service(gs, g) is True
    assert gs.money < money_before

    # Mejorar habitación y fachada (suben el ingreso).
    income_before = economy.total_income_per_sec(gs)
    assert actions.upgrade_room(gs, floor.rooms[0]) is True
    assert actions.upgrade_facade(gs) is True
    assert economy.total_income_per_sec(gs) > income_before

    # Tick idle: el dinero se acumula.
    money0 = gs.money
    for _ in range(10):
        session.apply_tick(gs, 1.0)
    assert gs.money > money0

    # Ascensor: reparar y subir al piso 2 (piso lleno + costo).
    gs.money = hotel.repair_cost(floor.index) + 1.0
    assert hotel.unlock_next_floor(gs, floor) is True
    assert len(gs.floors) == 2
    assert gs.floors[1].unlocked is True

    # Clicker de paquete: recompensa acotada.
    reward = idle.clicker_reward(25, economy.total_income_per_sec(gs))
    assert reward > 0

    # Guardado/offline: catch_up acredita el hueco.
    gs.last_seen = 1000.0
    credited = session.catch_up(gs, 1000.0 + 120.0)
    assert credited > 0
    assert gs.last_seen == 1000.0 + 120.0


def test_condition_room_refused_without_money():
    gs = state.new_game()
    floor = gs.floors[0]
    gs.money = 0.0
    assert hotel.condition_room(gs, floor, floor.rooms[0], state.Guest(name="X")) is False
    assert not floor.rooms[0].occupied
