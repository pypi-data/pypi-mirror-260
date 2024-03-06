""" pynchon.abcs
"""

from fleks.config import Config as FleksConfig  # noqa

from pynchon.util import typing  # noqa

from .attrdict import AttrDict  # noqa
from .path import Path  # noqa

ResourceType = typing.Union[str, Path]


class Config(FleksConfig):
    apply_hooks: typing.List[str] = typing.Field(default=[])
