import json

import yaml  # type: ignore
from yaml import Loader


class Dumper(yaml.Dumper):  # pylint: disable=too-many-ancestors
    """Custom dumper for correct indentation."""

    def increase_indent(self, flow=False, indentless=False):
        """Disable indentless."""
        return super().increase_indent(flow, False)


def yaml_dumper(content: str) -> str:
    """Convert a string into a YAML stream.

    Parameters
    ----------
    content: str
        Python object as string

    Returns
    -------
    str:
        YAML stream as string
    """
    return yaml.dump(
        yaml.load(json.dumps(content), Loader=Loader),
        Dumper=Dumper,
        default_flow_style=False,
    )
