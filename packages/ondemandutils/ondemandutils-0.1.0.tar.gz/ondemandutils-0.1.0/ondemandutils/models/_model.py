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

"""Macros and base methods for Open Ondemand data models."""

import copy
import inspect
import json
from functools import wraps
from typing import Any, Callable, Dict

import yaml


def assert_type(*typed_args, **typed_kwargs):
    """Check the type of args and kwargs passed to a function/method."""

    def decorator(func: Callable):
        sig = inspect.signature(func)
        bound_types = sig.bind_partial(*typed_args, **typed_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs).arguments
            for name in bound_types.keys() & bound_values.keys():
                if not isinstance(bound_values[name], bound_types[name]):
                    raise TypeError(f"{bound_values[name]} is not {bound_types[name]}.")

            return func(*args, **kwargs)

        return wrapper

    return decorator


# Generate descriptors for Open OnDemand configuration options.
# These descriptors are used for retrieving configuration values and
# provide an interface for CRUDing configuration options.
# The descriptors use an internal _register dictionary object to
# manage the parsed configuration options from Open OnDemand.
def base_descriptors(option: str):
    """Generate descriptors for accessing configuration option values.

    Args:
        option: Configuration option to generate descriptors for.
    """

    def getter(self):
        return self._register.get(option, None)

    def setter(self, value):
        self._register[option] = value

    def deleter(self):
        try:
            del self._register[option]
        except KeyError:
            pass

    return getter, setter, deleter


class BaseModel:
    """Base class for Open Ondemand-related data models."""

    def __init__(self, validator, **kwargs) -> None:
        for k, v in kwargs.items():
            if not hasattr(validator, k.upper()):
                raise AttributeError(
                    f"Unrecognised configuration option {k}={v}. "
                    + "Supported configurations include: "
                    + ", ".join(e.name.lower() for e in validator)
                )

        self._register = kwargs

    def __repr__(self):
        output = self._register
        return f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in output.items())})"

    @classmethod
    def from_dict(cls, dict_obj: Dict[str, Any]):
        """Construct data model object using a dictionary object."""
        return cls(**dict_obj)

    @classmethod
    def from_json(cls, json_obj: str):
        """Construct data model object using a JSON object."""
        data = json.loads(json_obj)
        return cls(**data)

    @classmethod
    def from_yaml(cls, yaml_doc: str):
        """Construct data model object using a YAML document."""
        data = yaml.safe_load(yaml_doc)
        return cls(**data)

    def dict(self) -> Dict[str, Any]:
        """Get model in dictionary form.

        Returns a deep copy of model's internal register. The deep copy is needed
        because assigned variables all point to the same dictionary in memory. Without the
        deep copy, operations performed on the returned dictionary could cause unintended
        mutations in the internal register.
        """
        return copy.deepcopy(self._register)

    def json(self) -> str:
        """Get model as JSON object."""
        return json.dumps(self._register)

    def yaml(self) -> str:
        """Get model as YAML document."""
        return yaml.dump(self._register)
