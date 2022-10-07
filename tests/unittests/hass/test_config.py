import pytest
from superbox_utils.config.exception import ConfigException
from superbox_utils.hass.config import HomeAssistantConfig


class TestHappyConfig:
    @pytest.mark.parametrize(
        "config, expected_enabled, expected_discovery_prefix",
        [
            (
                {"enabled": True, "discovery_prefix": "mocked-discovery-prefix"},
                True,
                "mocked-discovery-prefix",
            ),
        ],
    )
    def test_home_assistant_config(
        self,
        config: dict,
        expected_enabled: bool,
        expected_discovery_prefix: str,
    ):
        home_assistant_config = HomeAssistantConfig()
        home_assistant_config.update(config)

        assert isinstance(home_assistant_config.enabled, bool)
        assert isinstance(home_assistant_config.discovery_prefix, str)

        assert expected_enabled == home_assistant_config.enabled
        assert expected_discovery_prefix == home_assistant_config.discovery_prefix


class TestUnhappyConfig:
    @pytest.mark.parametrize(
        "config, expected_log",
        [
            (
                {"enabled": True, "discovery_prefix": "invalid discovery prefix"},
                "[HOMEASSISTANT] Invalid value 'invalid discovery prefix' in 'discovery_prefix'. The following characters are prohibited: a-z 0-9 -_",
            ),
        ],
    )
    def test_home_assistant_config(
        self,
        config: dict,
        expected_log: str,
    ):
        with pytest.raises(ConfigException) as error:
            home_assistant_config = HomeAssistantConfig()
            home_assistant_config.update(config)

        assert expected_log == str(error.value)
