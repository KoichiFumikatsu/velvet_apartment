# Velvet Apartment — punto de entrada.
# La navegación real (hub de recepción) se arma en bridge.rpy + reception.rpy.

label start:
    # Nueva partida: catch_up siembra last_seen y entra al hub de recepción.
    # (El intro narrativo completo llega en el plan de narrativa.)
    "Despiertas en el lobby. En recepción, tu contrato ya está firmado..."
    $ catch_up_now()
    jump hub
