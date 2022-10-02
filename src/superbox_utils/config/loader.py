import dataclasses
from dataclasses import dataclass
from dataclasses import is_dataclass
from pathlib import Path
from typing import Any

from superbox_utils.config.exception import ConfigException
from superbox_utils.yaml.loader import yaml_loader_safe


@dataclass
class ConfigMixin:
    def update(self, new):
        for key, value in new.items():
            if hasattr(self, key):
                item = getattr(self, key)

                if is_dataclass(item):
                    item.update(value)
                else:
                    setattr(self, key, value)

        self.validate()

    def update_from_yaml_file(self, config_path: Path):
        _config: dict = {}

        if config_path.exists():
            _config = yaml_loader_safe(config_path)

        self.update(_config)

    def validate(self):
        for f in dataclasses.fields(self):
            value: Any = getattr(self, f.name)

            if is_dataclass(value):
                value.validate()
            else:
                if method := getattr(self, f"_validate_{f.name}", None):
                    setattr(self, f.name, method(getattr(self, f.name), f=f))

                if not isinstance(value, f.type) and not is_dataclass(value):
                    raise ConfigException(f"Expected {f.name} to be {f.type}, got {repr(value)}")
