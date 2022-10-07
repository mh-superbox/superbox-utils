import pytest
from superbox_utils.argparse import argparse
from superbox_utils.argparse import init_argparse


class TestHappyPathArgparse:
    @pytest.mark.parametrize(
        "description, arguments, expected_log",
        [("DESCRIPTION", ["-vv"], "Namespace(verbose=2)")],
    )
    def test_init_argparse(self, description: str, arguments: list, expected_log: str):
        parser: argparse.ArgumentParser = init_argparse(description)
        args: argparse.Namespace = parser.parse_args(arguments)

        assert description == parser.prog
        assert expected_log == str(args)
