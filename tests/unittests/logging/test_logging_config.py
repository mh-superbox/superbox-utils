import pytest

from superbox_utils.config.exception import ConfigException
from superbox_utils.logging.config import LoggingConfig


class TestHappyLoggingConfig:
    @pytest.mark.parametrize(
        "config, expected_level, expected_verbose",
        [
            ({"level": "error"}, "error", 0),
            ({"level": "warning"}, "warning", 1),
            ({"level": "info"}, "info", 2),
            ({"level": "debug"}, "debug", 3),
        ],
    )
    def test_logging_config(
        self,
        config: dict,
        expected_level: str,
        expected_verbose: int,
    ):
        logging_config = LoggingConfig()
        logging_config.update(config)
        logging_config.update_level(name="test-logger")

        assert isinstance(logging_config.level, str)

        assert expected_level == logging_config.level
        assert expected_verbose == logging_config.verbose


class TestUnHappyLoggingConfig:
    @pytest.mark.parametrize(
        "config, expected_log",
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
        expected_log: str,
    ):
        with pytest.raises(ConfigException) as error:
            logging_config = LoggingConfig()
            logging_config.update(config)
            logging_config.update_level(name="test-logger")

        assert expected_log == str(error.value)
