from dataclasses import dataclass
from dataclasses import field
from dataclasses import is_dataclass
from pathlib import Path

import pytest

from superbox_utils.config.exception import ConfigException
from superbox_utils.config.loader import ConfigLoaderMixin
from superbox_utils.logging.config import LoggingConfig
from unittests.config.test_loader_data import CONFIG_INVALID_TYPE
from unittests.config.test_loader_data import CONFIG_LOGGING_INFO
from unittests.config.test_loader_data import CONFIG_LOGGING_WARNING


@dataclass
class Config(ConfigLoaderMixin):
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    features: dict = field(init=False, default_factory=dict)


class TestHappyPathLoader:
    @pytest.mark.parametrize(
        "_content_to_file, expected",
        [
            (("test.yaml", CONFIG_LOGGING_WARNING), "warning"),
            (("test.yaml", CONFIG_LOGGING_INFO), "info"),
        ],
        indirect=["_content_to_file"],
    )
    def test_config_loader(self, _content_to_file: Path, expected: str):
        config = Config()
        config.update_from_yaml_file(_content_to_file)

        assert config.logging.level == expected
        assert is_dataclass(config) is True
        assert str(config) == f"Config(logging=LoggingConfig(output='systemd', level='{expected}'), features={{}})"


class TestUnhappyPathLoader:
    @pytest.mark.parametrize(
        "_content_to_file, expected",
        [
            (("test.yaml", CONFIG_INVALID_TYPE), "Expected features to be <class 'dict'>, got 'invalid'"),
        ],
        indirect=["_content_to_file"],
    )
    def test_config_loader(self, _content_to_file: Path, expected: str):
        with pytest.raises(ConfigException) as error:
            config = Config()
            config.update_from_yaml_file(_content_to_file)

        assert str(error.value) == expected
