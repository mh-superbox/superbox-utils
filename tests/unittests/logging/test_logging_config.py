from pathlib import Path

import pytest

from superbox_utils.config.exception import ConfigException
from superbox_utils.logging.config import LoggingConfig


class TestHappyLoggingConfig:
    @pytest.mark.parametrize(
        "config, expected",
        [
            ({"output": "file", "level": "error"}, {"level": "error", "verbose": 0}),
            ({"output": "file", "level": "warning"}, {"level": "warning", "verbose": 1}),
            ({"output": "systemd", "level": "info"}, {"level": "info", "verbose": 2}),
            ({"output": "systemd", "level": "debug"}, {"level": "debug", "verbose": 3}),
        ],
    )
    def test_logging_config(
        self,
        tmp_path: Path,
        config: dict,
        expected: dict,
    ):
        logging_config = LoggingConfig()
        logging_config.update(config)
        logging_config.init(name="test-logger", log_path=tmp_path)

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
            logging_config.init(name="test-logger")

        assert str(error.value) == expected
