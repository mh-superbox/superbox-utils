import pytest
from superbox_utils.mqtt.config import MqttConfig


class TestHappyConfig:
    @pytest.mark.parametrize(
        "config, expected_mqtt_host, expected_mqtt_port, expected_keepalive, expected_retry_limit, expected_reconnect_interval",
        [
            (
                {"host": "mocked-host", "port": 1000, "keepalive": 20, "retry_limit": 40, "reconnect_interval": 20},
                "mocked-host",
                1000,
                20,
                40,
                20,
            ),
        ],
    )
    def test_mqtt_config(
        self,
        config: dict,
        expected_mqtt_host: str,
        expected_mqtt_port: int,
        expected_keepalive: int,
        expected_retry_limit: int,
        expected_reconnect_interval: int,
    ):
        mqtt_config = MqttConfig()
        mqtt_config.update(config)

        assert isinstance(mqtt_config.host, str)
        assert isinstance(mqtt_config.port, int)
        assert isinstance(mqtt_config.keepalive, int)
        assert isinstance(mqtt_config.retry_limit, int)
        assert isinstance(mqtt_config.reconnect_interval, int)

        assert expected_mqtt_host == mqtt_config.host
        assert expected_mqtt_port == mqtt_config.port
        assert expected_keepalive == mqtt_config.keepalive
        assert expected_retry_limit == mqtt_config.retry_limit
        assert expected_reconnect_interval == mqtt_config.reconnect_interval
