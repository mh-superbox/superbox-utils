import pytest

from superbox_utils.yaml.dumper import yaml_dumper
from unittests.yaml.test_dumper_data import JSON_STRING
from unittests.yaml.test_dumper_data import YAML_STRING


class TestHappyPathDumper:
    @pytest.mark.parametrize(
        "json_content, expected",
        [
            (JSON_STRING, YAML_STRING),
        ],
    )
    def test_yaml_dumper(self, json_content: str, expected: str) -> None:
        assert yaml_dumper(json_content) == expected
