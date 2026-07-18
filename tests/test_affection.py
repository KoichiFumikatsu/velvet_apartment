from velvet import affection, state


def test_current_tier_boundaries():
    assert affection.current_tier(0) == "SFW"
    assert affection.current_tier(24) == "SFW"
    assert affection.current_tier(25) == "SUGGESTIVE"
    assert affection.current_tier(60) == "NSFW"
    assert affection.current_tier(90) == "NSFW_NOCTURNO"
    assert affection.current_tier(100) == "NSFW_NOCTURNO"


def test_unlocked_tiers_accumulate():
    assert affection.unlocked_tiers(0) == ["SFW"]
    assert affection.unlocked_tiers(61) == ["SFW", "SUGGESTIVE", "NSFW"]


def test_add_affection_clamps():
    g = state.Guest(name="G", affection=95)
    affection.add_affection(g, 20)
    assert g.affection == 100.0
    affection.add_affection(g, -500)
    assert g.affection == 0.0
