# Copyright 2024 Canonical Ltd.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

"""Edit `nginx_stage.yml` configuration files."""

__all__ = ["dump", "dumps", "load", "loads", "edit"]

import os
from contextlib import contextmanager
from datetime import datetime
from functools import partial
from typing import Union

from ondemandutils.models import NginxStageConfig

from ._editor import dump_base, dumps_base, header, load_base, loads_base


def _marshaller(config: NginxStageConfig) -> str:
    """Marshall `NginxStageConfig` object into an `nginx_stage.yml` configuration file.

    Args:
        config: `NginxStageConfig` object to marshal into configuration file.
    """
    marshalled = header(f"`nginx_stage.yml` generated at {datetime.now()} by ondemandutils.")
    marshalled += "\n" + config.yaml()
    return marshalled


def _parser(config: str) -> NginxStageConfig:
    """Parse `nginx_stage.yml` configuration file into `NginxStageConfig` object.

    Args:
        config: Content of `nginx_stage.yml` configuration file.
    """
    return NginxStageConfig.from_yaml(config)


dump = partial(dump_base, marshaller=_marshaller)
dump.__doc__ = """
Serialise an `NginxStageConfig` object into a YAML document file.

Args:
    obj: `NginxStageConfig` object to serialise into a YAML document.
    file: File to serialise `NginxStageConfig` object into.
"""

dumps = partial(dumps_base, marshaller=_marshaller)
dumps.__doc__ = """
Serialise an `NginxStageConfig` object into a YAML document string.

Args:
    obj: `NginxStageConfig` object to serialise into a YAML document.
"""

load = partial(load_base, parser=_parser)
load.__doc__ = """
Deserialise a YAML document file into an `NginxStageConfig` object.

Args:
    file: `nginx_stage.yml` file to deserialise into an `NginxStageConfig` object.
"""

loads = partial(loads_base, parser=_parser)
loads.__doc__ = """
Deserialise a YAML document string into an `NginxStageConfig` object.

Args:
    content: String content to deserialise into an `NginxStageConfig` object.
"""


@contextmanager
def edit(file: Union[str, os.PathLike]) -> NginxStageConfig:
    """Edit an `nginx_stage.yml` configuration file.

    Args:
        file: File path to `nginx_stage.yml`. If `nginx_stage.yml` does not exist
            at the given path, a blank `nginx_stage.yml` will be created.
    """
    if not os.path.exists(file):
        config = NginxStageConfig()
    else:
        config = load(file=file)

    yield config
    dump(content=config, file=file)
