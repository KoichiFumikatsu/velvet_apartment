import pytest

from velvet import display, state


def test_abbreviate_ranges():
    assert display.abbreviate(0) == "0"
    assert display.abbreviate(999) == "999"
    assert display.abbreviate(1234) == "1.23K"
    assert display.abbreviate(1_500_000) == "1.50M"
    assert display.abbreviate(2_000_000_000) == "2.00B"


def test_format_money_prefixes_dollar():
    assert display.format_money(1234) == "$1.23K"
    assert display.format_money(50) == "$50"


def test_affection_fraction_clamps_0_1():
    g = state.Guest(name="G", affection=50)
    assert display.affection_fraction(g) == pytest.approx(0.5)
    g.affection = 200
    assert display.affection_fraction(g) == 1.0
    g.affection = -10
    assert display.affection_fraction(g) == 0.0


def test_tier_display_names():
    assert display.tier_display(state.Guest(name="G", affection=0)) == "SFW"
    assert display.tier_display(state.Guest(name="G", affection=25)) == "Sugerente"
    assert display.tier_display(state.Guest(name="G", affection=90)) == "NSFW Nocturno"


def test_door_label_occupied_vs_empty():
    assert display.door_label(state.Room()) == "Vacía"
    assert display.door_label(state.Room(guest=state.Guest(name="Amber-like"))) == "Amber-like"


def test_income_and_cost_labels():
    assert display.room_income_label(12) == "$12/s"
    assert display.cost_label(1500) == "$1.50K"
