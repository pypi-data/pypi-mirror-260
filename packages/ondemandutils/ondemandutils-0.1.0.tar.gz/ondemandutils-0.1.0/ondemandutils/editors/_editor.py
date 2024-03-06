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
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Base methods for Open Ondemand configuration file editors."""

import logging
from os import PathLike
from pathlib import Path
from typing import Union

_logger = logging.getLogger(__name__)


def header(msg: str) -> str:
    """Generate header for YAML document file.

    Args:
        msg: Message to put into header.
    """
    return "#\n" + "".join(f"# {line}\n" for line in msg.splitlines()) + "#\n"


def dump_base(content, file: Union[str, PathLike], marshaller):
    """Dump configuration into file using provided marshalling function.

    Do not use this function directly.
    """
    if (loc := Path(file)).exists():
        _logger.warning("Overwriting contents of %s file located at %s.", loc.name, loc)

    _logger.debug("Marshalling configuration into %s file located at %s.", loc.name, loc)
    return loc.write_text(marshaller(content), encoding="ascii")


def dumps_base(content, marshaller) -> str:
    """Dump configuration into Python string using provided marshalling function.

    Do not use this function directly.
    """
    return marshaller(content)


def load_base(file: Union[str, PathLike], parser):
    """Load configuration from file using provided parsing function.

    Do not use this function directly.
    """
    if (file := Path(file)).exists():
        _logger.debug("Parsing contents of %s located at %s.", file.name, file)
        config = file.read_text(encoding="ascii")
        return parser(config)
    else:
        msg = "Unable to locate file"
        _logger.error(msg + " %s.", file)
        raise FileNotFoundError(msg + f" {file}")


def loads_base(content: str, parser):
    """Load configuration from Python String using provided parsing function.

    Do not use this function directly.
    """
    return parser(content)
