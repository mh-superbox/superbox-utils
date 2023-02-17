import pytest

from superbox_utils.mqtt.config import MqttConfig


class TestHappyConfig:
    @pytest.mark.parametrize(
        "config, expected",
        [
            (
                {"host": "mocked-host", "port": 1000, "keepalive": 20, "retry_limit": 40, "reconnect_interval": 20},
                {"host": "mocked-host", "port": 1000, "keepalive": 20, "retry_limit": 40, "reconnect_interval": 20},
            ),
        ],
    )
    def test_mqtt_config(self, config: dict, expected: dict) -> None:
        mqtt_config = MqttConfig()
        mqtt_config.update(config)

        assert isinstance(mqtt_config.host, str)
        assert isinstance(mqtt_config.port, int)
        assert isinstance(mqtt_config.keepalive, int)
        assert isinstance(mqtt_config.retry_limit, int)
        assert isinstance(mqtt_config.reconnect_interval, int)

        assert mqtt_config.host == expected["host"]
        assert mqtt_config.port == expected["port"]
        assert mqtt_config.keepalive == expected["keepalive"]
        assert mqtt_config.retry_limit == expected["retry_limit"]
        assert mqtt_config.reconnect_interval == expected["reconnect_interval"]
