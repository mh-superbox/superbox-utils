import dataclasses
import logging
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import List

from superbox_utils.config.exception import ConfigException
from superbox_utils.config.loader import ConfigLoaderMixin
from superbox_utils.logging import DEFAULT_LOG_FORMAT
from superbox_utils.logging import FILE_LOG_FORMAT
from superbox_utils.logging import LOG_LEVEL


@dataclass
class LoggingConfig(ConfigLoaderMixin):
    output: str = field(default="systemd")
    level: str = field(default="error")

    @property
    def verbose(self) -> int:
        """Get logging verbose level as integer."""
        return list(LOG_LEVEL).index(self.level)

    def init(self, name: str, log_path: Path):
        """Initialize logger handler and formatter.

        Parameters
        ----------
        name: str
            The logger name.
        log_path: Path
            custom log path.
        """
        logger: logging.Logger = logging.getLogger(name)
        logger.setLevel(LOG_LEVEL["info"])

        c_handler = logging.StreamHandler()
        c_handler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))

        if self.output == "systemd":
            c_handler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))
        else:
            c_handler.setFormatter(logging.Formatter(FILE_LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))

        logger.addHandler(c_handler)

        if self.output == "file":
            log_path.mkdir(exist_ok=True, parents=True)

            f_handler = logging.FileHandler(log_path / f"{name}.log")
            f_handler.setFormatter(logging.Formatter(FILE_LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
            logger.addHandler(f_handler)

        self.update_level(name)

    def update_level(self, name: str, verbose: int = 0):
        """Update the logging level in config data class.

        Parameters
        ----------
        name: str
            The logger name.
        verbose: int
            Logging verbose level as integer.
        """
        logger: logging.Logger = logging.getLogger(name)

        levels: List[int] = list(LOG_LEVEL.values())
        level: int = levels[min(max(verbose, self.verbose), len(levels) - 1)]

        logger.setLevel(level)

    def _validate_level(self, value: str, _field: dataclasses.Field) -> str:
        if (value := value.lower()) not in LOG_LEVEL.keys():
            raise ConfigException(
                f"[{self.__class__.__name__.replace('Config', '').upper()}] Invalid log level '{self.level}'. The following log levels are allowed: {' '.join(LOG_LEVEL.keys())}."
            )

        return value
