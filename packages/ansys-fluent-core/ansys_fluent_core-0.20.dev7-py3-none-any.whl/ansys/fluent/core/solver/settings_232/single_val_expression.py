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

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .single_val_expression_child import single_val_expression_child

class single_val_expression(NamedObject[single_val_expression_child], _CreatableNamedObjectMixin[single_val_expression_child]):
    """
    'single_val_expression' child.
    """

    fluent_name = "single-val-expression"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: single_val_expression_child = single_val_expression_child
    """
    child_object_type of single_val_expression.
    """
