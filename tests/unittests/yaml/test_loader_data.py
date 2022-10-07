from typing import Final

VALID_YAML: Final[
    str
] = """key1: value1
key2: value2
"""

INVALID_YAML: Final[
    str
] = """key1: value1
key2
"""
