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

from .global_range import global_range as global_range_cls
class auto_range_on(Group):
    """
    Auto calculate the minimum and maximum values of the scalar field will be the limits of that
    field.
    """

    fluent_name = "auto-range-on"

    child_names = \
        ['global_range']

    _child_classes = dict(
        global_range=global_range_cls,
    )

