from velvet import guests


def test_amber_name_single_source():
    g = guests.make_amber()
    assert g.name == guests.AMBER_NAME == "Amber"
    assert g.affection == 0.0


def test_visit_line_by_tier():
    assert guests.amber_visit_line(0.0) == guests.AMBER_LINES["SFW"]
    assert guests.amber_visit_line(30.0) == guests.AMBER_LINES["SUGGESTIVE"]


def test_lines_cover_all_tiers():
    from velvet import config
    assert set(guests.AMBER_LINES) == set(config.TIER_THRESHOLDS)
