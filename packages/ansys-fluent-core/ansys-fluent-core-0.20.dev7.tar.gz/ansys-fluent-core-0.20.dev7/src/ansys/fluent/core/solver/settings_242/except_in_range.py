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

from .value1 import value1 as value1_cls
from .value2 import value2 as value2_cls
class except_in_range(Group):
    """
    'except_in_range' child.
    """

    fluent_name = "except-in-range"

    child_names = \
        ['value1', 'value2']

    _child_classes = dict(
        value1=value1_cls,
        value2=value2_cls,
    )

