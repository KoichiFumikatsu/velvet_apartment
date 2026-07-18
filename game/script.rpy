# Velvet Apartment — punto de entrada.
# La navegación real (hub de recepción) se arma en bridge.rpy + reception.rpy.

label start:
    # Nueva partida: catch_up siembra last_seen y entra al hub de recepción.
    # (El intro narrativo completo llega en el plan de narrativa.)
    "Despiertas en el lobby. En recepción, tu contrato ya está firmado..."
    # Capital inicial para acondicionar la primera habitación y arrancar el ciclo idle.
    $ gs.money = velvet.config.STARTING_MONEY
    $ catch_up_now()
    jump hub
