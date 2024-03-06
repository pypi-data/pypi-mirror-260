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

from .pattern import pattern as pattern_cls
from .weight_1 import weight as weight_cls
from .color_1 import color as color_cls
class line_in_file(Group):
    """
    Set parameters for plot lines (file).
    """

    fluent_name = "line-in-file"

    child_names = \
        ['pattern', 'weight', 'color']

    _child_classes = dict(
        pattern=pattern_cls,
        weight=weight_cls,
        color=color_cls,
    )

