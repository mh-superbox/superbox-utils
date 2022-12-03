from pathlib import Path
from typing import Optional

import pytest

from superbox_utils.config.exception import ConfigException
from superbox_utils.logging.config import LoggingConfig


class TestHappyLoggingConfig:
    @pytest.mark.parametrize(
        "config, log, expected",
        [
            ({"level": "error"}, "systemd", {"level": "error", "verbose": 0}),
            ({"level": "warning"}, "file", {"level": "warning", "verbose": 1}),
            ({"level": "info"}, None, {"level": "info", "verbose": 2}),
            ({"level": "debug"}, None, {"level": "debug", "verbose": 3}),
        ],
    )
    def test_logging_config(
        self,
        tmp_path: Path,
        config: dict,
        log: Optional[str],
        expected: dict,
    ):
        logging_config = LoggingConfig()
        logging_config.update(config)
        logging_config.init(name="test-logger", log=log, log_path=tmp_path)

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
        tmp_path: Path,
        config: dict,
        expected: str,
    ):
        with pytest.raises(ConfigException) as error:
            logging_config = LoggingConfig()
            logging_config.update(config)
            logging_config.init(name="test-logger", log_path=tmp_path)

        assert str(error.value) == expected
