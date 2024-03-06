#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    _CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    _HasAllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .enabled_15 import enabled as enabled_cls
from .color_1 import color as color_cls
class constant_color(Group):
    """
    'constant_color' child.
    """

    fluent_name = "constant-color"

    child_names = \
        ['enabled', 'color']

    _child_classes = dict(
        enabled=enabled_cls,
        color=color_cls,
    )

