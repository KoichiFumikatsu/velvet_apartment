from velvet import state, tutorial


def _fresh():
    gs = state.new_game()
    gs.floors[0].rooms[0].guest = state.Guest(name="Amber")
    return gs


def test_starts_at_first_step():
    gs = _fresh()
    assert gs.tutorial_step == 0
    assert gs.tutorial_done is False
    assert tutorial.current_text(gs) == tutorial.STEPS[0][0]


def test_advances_after_visit():
    gs = _fresh()
    assert tutorial.advance(gs) is False          # nada hecho aún
    assert gs.tutorial_step == 0
    gs.floors[0].rooms[0].guest.affection = 5.0    # visitó
    assert tutorial.advance(gs) is False           # pasa a paso 1, no completa
    assert gs.tutorial_step == 1
    assert tutorial.current_text(gs) == tutorial.STEPS[1][0]


def test_completes_after_upgrade():
    gs = _fresh()
    gs.floors[0].rooms[0].guest.affection = 5.0
    gs.floors[0].rooms[0].upgrade_level = 2
    assert tutorial.advance(gs) is True            # transición a completo
    assert gs.tutorial_done is True
    assert tutorial.current_text(gs) is None


def test_does_not_skip_steps():
    gs = _fresh()
    gs.floors[0].rooms[0].upgrade_level = 2         # upgrade sin visitar primero
    assert tutorial.advance(gs) is False
    assert gs.tutorial_step == 0                     # el gate del paso 0 no se cumplió


def test_idempotent_when_done():
    gs = _fresh()
    gs.tutorial_done = True
    assert tutorial.advance(gs) is False
    assert tutorial.current_text(gs) is None
