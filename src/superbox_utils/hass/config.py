import dataclasses
import re
from dataclasses import dataclass
from dataclasses import field
from re import Match
from typing import Optional

from superbox_utils.config.exception import ConfigException
from superbox_utils.config.loader import ConfigLoaderMixin
from superbox_utils.config.loader import Validation


@dataclass
class HomeAssistantConfig(ConfigLoaderMixin):
    enabled: bool = field(default=True)
    discovery_prefix: str = field(default="homeassistant")

    def _validate_discovery_prefix(self, value: str, f: dataclasses.Field) -> str:
        value = value.lower()
        result: Optional[Match[str]] = re.search(Validation.ALLOWED_CHARACTERS.regex, value)

        if result is None:
            raise ConfigException(
                f"[{self.__class__.__name__.replace('Config', '').upper()}] Invalid value '{value}' in '{f.name}'. {Validation.ALLOWED_CHARACTERS.error}"
            )

        return value
