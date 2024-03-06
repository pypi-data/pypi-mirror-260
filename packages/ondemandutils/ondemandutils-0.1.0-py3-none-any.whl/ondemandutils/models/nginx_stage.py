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

"""Data models for the `nginx_stage.yml` configuration file."""

from ._model import BaseModel, base_descriptors
from ._options import NginxStageOptions


class NginxStageConfig(BaseModel):
    """Data model representing the `nginx_stage.yml` configuration file."""

    def __init__(self, **kwargs) -> None:
        super().__init__(validator=NginxStageOptions, **kwargs)


# Generate descriptors for accessing `nginx_stage.yml` configuration options.
for e in NginxStageOptions:
    attr_name = e.name.lower()
    setattr(NginxStageConfig, attr_name, property(*base_descriptors(attr_name)))
