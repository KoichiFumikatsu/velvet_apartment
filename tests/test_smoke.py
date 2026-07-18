from velvet import config


def test_config_imports():
    assert config.ROOM_UPGRADE_GROWTH == 1.15
    assert config.TIER_THRESHOLDS["NSFW_NOCTURNO"] == 90.0
