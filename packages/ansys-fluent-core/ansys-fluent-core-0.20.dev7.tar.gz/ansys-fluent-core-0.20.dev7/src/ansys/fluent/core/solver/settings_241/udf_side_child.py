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

from .name import name as name_cls
from .value_1 import value as value_cls
class udf_side_child(Group):
    """
    'child_object_type' of udf_side.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'value']

    _child_classes = dict(
        name=name_cls,
        value=value_cls,
    )

