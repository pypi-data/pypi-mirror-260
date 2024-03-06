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
from .apply_function import apply_function as apply_function_cls
class scheme_proc_child(Group):
    """
    'child_object_type' of scheme_proc.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'value', 'apply_function']

    _child_classes = dict(
        name=name_cls,
        value=value_cls,
        apply_function=apply_function_cls,
    )

