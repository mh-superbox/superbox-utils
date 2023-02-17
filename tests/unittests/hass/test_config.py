import pytest

from superbox_utils.config.exception import ConfigException
from superbox_utils.hass.config import HomeAssistantConfig


class TestHappyConfig:
    @pytest.mark.parametrize(
        "config, expected",
        [
            (
                {"enabled": True, "discovery_prefix": "mocked-discovery-prefix"},
                {"enabled": True, "discovery_prefix": "mocked-discovery-prefix"},
            ),
        ],
    )
    def test_home_assistant_config(
        self,
        config: dict,
        expected: dict,
    ) -> None:
        home_assistant_config = HomeAssistantConfig()
        home_assistant_config.update(config)

        assert isinstance(home_assistant_config.enabled, bool)
        assert isinstance(home_assistant_config.discovery_prefix, str)

        assert home_assistant_config.enabled == expected["enabled"]
        assert home_assistant_config.discovery_prefix == expected["discovery_prefix"]


class TestUnhappyConfig:
    @pytest.mark.parametrize(
        "config, expected",
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
        expected: str,
    ) -> None:
        with pytest.raises(ConfigException) as error:
            home_assistant_config = HomeAssistantConfig()
            home_assistant_config.update(config)

        assert str(error.value) == expected
