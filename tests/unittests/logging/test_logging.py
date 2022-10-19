import logging

import pytest

from superbox_utils.logging import init_logger
from superbox_utils.logging import stream_handler


class TestHappyPathLogging:
    @pytest.mark.parametrize(
        "log_level, expected",
        [
            ("error", logging.ERROR),
            ("warning", logging.WARNING),
            ("info", logging.INFO),
            ("debug", logging.DEBUG),
        ],
    )
    def test_init_logger(self, log_level: str, expected: int):
        logger: logging.Logger = init_logger(name="test-logger", level=log_level, handlers=[stream_handler])

        assert logger.level == expected
        assert logger.name == "test-logger"
        assert isinstance(logger.handlers[0], logging.StreamHandler)
