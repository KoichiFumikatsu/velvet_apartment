# intro.rpy — intro VN (cómica, lineal, voz interna) + siembra de Amber + tutorial.
# Arte = placeholders (scene black); los CG/fondos IA Gen llegan en Contenido.

define amber = Character("Amber", color="#ffb0b0")

label start:
    scene black with fade
    "Tres meses sin empleo. Mi currículum ya daba lástima hasta a mí."
    "Y entonces apareció el anuncio."
    "'Recepcionista nocturno. Sin experiencia. Sueldo: obsceno. Alojamiento incluido.'"
    "Cualquiera con dos dedos de frente habría desconfiado."
    "Yo tenía hambre. Fui."

    scene black
    "La entrevista fue en un edificio que no salía en ningún mapa."
    "El tipo sonreía demasiado. Me ofreció un té."
    "Recuerdo el primer sorbo. Después... nada."
    "..."

    scene black with fade
    "Desperté detrás de un mostrador."
    "Un lobby enorme. Terciopelo por todas partes. Silencio."
    "Sobre el mostrador, un contrato. Firmado. Con mi letra."
    "No recuerdo haberlo firmado."
    "Cláusula única, en negrita: mantener contentas a las huéspedes del hotel."
    "Debería estar aterrado. Pero el sueldo seguía siendo obsceno, así que decidí no hacer preguntas."

    # Siembra del estado narrativo (capital inicial + Amber en la habitación 1).
    $ gs.money = velvet.config.STARTING_MONEY
    $ gs.floors[0].rooms[0].guest = velvet.guests.make_amber()
    $ gs.tutorial_step = 0
    $ gs.tutorial_done = False

    # Presentación de la 1ª huésped.
    "El ascensor sonó. De él bajó una pelirroja con un lazo enorme y demasiada energía."
    amber "¡Holaaa! ¿Tú eres el nuevo? Perfecto, esto estaba MUERTO."
    "La reconocí al instante. No de la vida real. De... otro sitio. Da igual."
    amber "Soy Amber. Habitación uno. Voy a ser tu favorita, ya lo verás."
    amber "Es fácil: te das una vuelta por el Pasillo, me visitas, y con lo que genere el hotel mejoras mi cuarto."
    "Un contrato que no firmé y una huésped que salió de un videojuego. Facilísimo."

    $ catch_up_now()
    jump hub
