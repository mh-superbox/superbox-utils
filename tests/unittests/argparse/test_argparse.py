import pytest

from superbox_utils.argparse import argparse
from superbox_utils.argparse import init_argparse


class TestHappyPathArgparse:
    @pytest.mark.parametrize(
        "description, arguments, expected",
        [("DESCRIPTION", ["-vv"], "Namespace(log='stdout', verbose=2)")],
    )
    def test_init_argparse(self, description: str, arguments: list, expected: str) -> None:
        parser: argparse.ArgumentParser = init_argparse(description)
        args: argparse.Namespace = parser.parse_args(arguments)

        assert parser.description == description
        assert str(args) == expected
