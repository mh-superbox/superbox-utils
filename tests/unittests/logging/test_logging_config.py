import logging
import re
import uuid
from pathlib import Path
from typing import Optional

import pytest
from _pytest.capture import CaptureFixture  # pylint: disable=import-private-name
from superbox_utils.config.exception import ConfigException
from superbox_utils.logging.config import LoggingConfig


class TestHappyLoggingConfig:
    @pytest.mark.parametrize(
        "config, log, expected",
        [
            ({"level": "error"}, "systemd", {"level": "error", "verbose": 0, "message": r"^<3>MOCKED ERROR\n$"}),
            ({"level": "error"}, "stdout", {"level": "error", "verbose": 0, "message": r"^MOCKED ERROR\n$"}),
            (
                {"level": "warning"},
                "file",
                {
                    "level": "warning",
                    "verbose": 1,
                    "message": r"^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2} \| ERROR \| MOCKED ERROR\n$",
                },
            ),
            (
                {"level": "info"},
                None,
                {
                    "level": "info",
                    "verbose": 2,
                    "message": r"^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2} \| ERROR \| MOCKED ERROR\n$",
                },
            ),
            (
                {"level": "debug"},
                None,
                {
                    "level": "debug",
                    "verbose": 3,
                    "message": r"^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2} \| ERROR \| MOCKED ERROR\n$",
                },
            ),
        ],
    )
    def test_logging_config(
        self, tmp_path: Path, config: dict, log: Optional[str], expected: dict, capsys: CaptureFixture
    ) -> None:
        uniqid = str(uuid.uuid4())
        logger: logging.Logger = logging.getLogger(uniqid)

        logging_config = LoggingConfig()
        logging_config.update(config)
        logging_config.init(name=uniqid, log=log, log_path=tmp_path)

        logger.error("MOCKED ERROR")

        log_file: Path = tmp_path / f"{uniqid}.log"

        if log == "file":
            assert log_file.exists()
            assert re.compile(expected["message"]).search(log_file.read_text())
        else:
            assert not log_file.exists()
            assert re.compile(expected["message"]).search(capsys.readouterr().err)

        assert isinstance(logging_config.level, str)

        assert logging_config.level == expected["level"]
        assert logging_config.verbose == expected["verbose"]


class TestUnHappyLoggingConfig:
    @pytest.mark.parametrize(
        "config, log, expected",
        [
            (
                {"level": "invalid"},
                "systemd",
                "[LOGGING] Invalid log level 'invalid'. The following log levels are allowed: error warning info debug.",
            ),
        ],
    )
    def test_logging_config(
        self,
        tmp_path: Path,
        config: dict,
        log: Optional[str],
        expected: str,
    ) -> None:
        with pytest.raises(ConfigException) as error:
            logging_config = LoggingConfig()
            logging_config.update(config)
            logging_config.init(name="test-logger", log=log, log_path=tmp_path)

        assert str(error.value) == expected
