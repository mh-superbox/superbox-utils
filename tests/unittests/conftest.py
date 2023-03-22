from pathlib import Path

import pytest
from _pytest.fixtures import SubRequest  # pylint: disable=import-private-name


@pytest.fixture()
def _content_to_file(request: SubRequest, tmp_path: Path) -> Path:
    content_path: Path = tmp_path / request.param[0]

    with open(content_path, "w", encoding="utf-8") as f:
        f.write(request.param[1])

    return content_path
