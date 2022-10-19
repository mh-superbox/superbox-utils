from pathlib import Path
from typing import Union

import pytest

from superbox_utils.config.exception import ConfigException
from superbox_utils.yaml.loader import yaml_loader_safe
from unittests.yaml.test_loader_data import INVALID_YAML
from unittests.yaml.test_loader_data import VALID_YAML


class TestHappyPathLoader:
    @pytest.mark.parametrize(
        "content_to_file, expected",
        [
            (("test.yaml", VALID_YAML), dict),
        ],
        indirect=["content_to_file"],
    )
    def test_yaml_loader_safe(self, content_to_file: Path, expected: type):
        yaml_data: Union[dict, list] = yaml_loader_safe(content_to_file)
        print(yaml_data)

        assert isinstance(yaml_data, expected)


class TestUnHappyPathLoader:
    @pytest.mark.parametrize(
        "content_to_file, expected",
        [
            (
                ("test.yaml", INVALID_YAML),
                """Can't read YAML file!\n  in "<unicode string>", line 3, column 1:\n    \n    ^""",
            ),
        ],
        indirect=["content_to_file"],
    )
    def test_yaml_loader_safe(self, content_to_file: Path, expected: str):
        with pytest.raises(ConfigException) as error:
            yaml_loader_safe(content_to_file)

        assert str(error.value) == expected
