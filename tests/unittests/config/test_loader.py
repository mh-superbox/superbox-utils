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
        "content_to_file, expected_log_level",
        [
            (("test.yaml", CONFIG_LOGGING_WARNING), "warning"),
            (("test.yaml", CONFIG_LOGGING_INFO), "info"),
        ],
        indirect=["content_to_file"],
    )
    def test_config_loader(self, content_to_file: Path, expected_log_level: str):
        config = Config()
        config.update_from_yaml_file(content_to_file)

        assert expected_log_level == config.logging.level
        assert True is is_dataclass(config)
        assert f"Config(logging=LoggingConfig(level='{expected_log_level}'), features={{}})" == str(config)


class TestUnhappyPathLoader:
    @pytest.mark.parametrize(
        "content_to_file, expected_log",
        [
            (("test.yaml", CONFIG_INVALID_TYPE), "Expected features to be <class 'dict'>, got 'invalid'"),
        ],
        indirect=["content_to_file"],
    )
    def test_config_loader(self, content_to_file: Path, expected_log: str):
        with pytest.raises(ConfigException) as error:
            config = Config()
            config.update_from_yaml_file(content_to_file)

        assert expected_log == str(error.value)
