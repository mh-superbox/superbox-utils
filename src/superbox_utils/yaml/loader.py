from pathlib import Path
from typing import Union

import yaml

from superbox_utils.config.exception import ConfigException


def yaml_loader_safe(yaml_file: Path) -> Union[dict, list]:
    try:
        return yaml.load(yaml_file.read_text(), Loader=yaml.FullLoader)
    except yaml.MarkedYAMLError as e:
        raise ConfigException(f"Can't read YAML file!\n{str(e.problem_mark)}")
