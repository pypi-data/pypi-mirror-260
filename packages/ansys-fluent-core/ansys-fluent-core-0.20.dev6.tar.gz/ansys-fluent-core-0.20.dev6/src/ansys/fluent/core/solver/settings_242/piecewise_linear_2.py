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

from .function_of import function_of as function_of_cls
from .data_points import data_points as data_points_cls
class piecewise_linear(Group):
    """
    Specify ranges and values for piecewise-linear property.
    """

    fluent_name = "piecewise-linear"

    child_names = \
        ['function_of', 'data_points']

    _child_classes = dict(
        function_of=function_of_cls,
        data_points=data_points_cls,
    )

