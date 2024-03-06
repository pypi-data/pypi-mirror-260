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

from .name_2 import name as name_cls
from .list_valid_report_names import list_valid_report_names as list_valid_report_names_cls
from .define import define as define_cls
from .expr_value import expr_value as expr_value_cls
from .average_over import average_over as average_over_cls
from .old_props import old_props as old_props_cls
class expression_child(Group):
    """
    'child_object_type' of expression.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'list_valid_report_names', 'define', 'expr_value',
         'average_over', 'old_props']

    _child_classes = dict(
        name=name_cls,
        list_valid_report_names=list_valid_report_names_cls,
        define=define_cls,
        expr_value=expr_value_cls,
        average_over=average_over_cls,
        old_props=old_props_cls,
    )

