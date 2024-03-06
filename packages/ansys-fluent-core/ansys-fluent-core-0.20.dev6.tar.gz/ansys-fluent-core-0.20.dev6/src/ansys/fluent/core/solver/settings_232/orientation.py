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

from .first_axis import first_axis as first_axis_cls
from .second_axis import second_axis as second_axis_cls
from .auto_second_axis import auto_second_axis as auto_second_axis_cls
class orientation(Group):
    """
    'orientation' child.
    """

    fluent_name = "orientation"

    child_names = \
        ['first_axis', 'second_axis', 'auto_second_axis']

    _child_classes = dict(
        first_axis=first_axis_cls,
        second_axis=second_axis_cls,
        auto_second_axis=auto_second_axis_cls,
    )

