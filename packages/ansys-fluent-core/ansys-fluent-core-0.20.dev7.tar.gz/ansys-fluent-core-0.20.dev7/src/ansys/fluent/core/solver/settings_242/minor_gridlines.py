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

from .color import color as color_cls
from .weight import weight as weight_cls
class minor_gridlines(Group):
    """
    Set properties of gridlines on axis.
    """

    fluent_name = "minor-gridlines"

    child_names = \
        ['color', 'weight']

    _child_classes = dict(
        color=color_cls,
        weight=weight_cls,
    )

