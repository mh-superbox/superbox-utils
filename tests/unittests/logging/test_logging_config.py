import pytest

from superbox_utils.config.exception import ConfigException
from superbox_utils.logging.config import LoggingConfig


class TestHappyLoggingConfig:
    @pytest.mark.parametrize(
        "config, expected",
        [
            ({"level": "error"}, {"level": "error", "verbose": 0}),
            ({"level": "warning"}, {"level": "warning", "verbose": 1}),
            ({"level": "info"}, {"level": "info", "verbose": 2}),
            ({"level": "debug"}, {"level": "debug", "verbose": 3}),
        ],
    )
    def test_logging_config(
        self,
        config: dict,
        expected: dict,
    ):
        logging_config = LoggingConfig()
        logging_config.update(config)
        logging_config.update_level(name="test-logger")

        assert isinstance(logging_config.level, str)

        assert logging_config.level == expected["level"]
        assert logging_config.verbose == expected["verbose"]


class TestUnHappyLoggingConfig:
    @pytest.mark.parametrize(
        "config, expected",
        [
            (
                {"level": "invalid"},
                "[LOGGING] Invalid log level 'invalid'. The following log levels are allowed: error warning info debug.",
            ),
        ],
    )
    def test_logging_config(
        self,
        config: dict,
        expected: str,
    ):
        with pytest.raises(ConfigException) as error:
            logging_config = LoggingConfig()
            logging_config.update(config)
            logging_config.update_level(name="test-logger")

        assert str(error.value) == expected
