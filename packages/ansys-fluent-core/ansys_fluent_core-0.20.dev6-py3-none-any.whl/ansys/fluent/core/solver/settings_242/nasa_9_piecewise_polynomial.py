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
from .range import range as range_cls
class nasa_9_piecewise_polynomial(Group):
    """
    'nasa_9_piecewise_polynomial' child.
    """

    fluent_name = "nasa-9-piecewise-polynomial"

    child_names = \
        ['function_of', 'range']

    _child_classes = dict(
        function_of=function_of_cls,
        range=range_cls,
    )

