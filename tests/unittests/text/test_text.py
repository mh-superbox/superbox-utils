import pytest

from superbox_utils.text.text import slugify


class TestHappyPathText:
    @pytest.mark.parametrize(
        "text, expected",
        [
            ("test", "test"),
            ("österreich", "osterreich"),
            ("space in text", "space_in_text"),
            ("UPPER and lower case", "upper_and_lower_case"),
        ],
    )
    def test_slugify(self, text: str, expected: str) -> None:
        assert slugify(text) == expected
