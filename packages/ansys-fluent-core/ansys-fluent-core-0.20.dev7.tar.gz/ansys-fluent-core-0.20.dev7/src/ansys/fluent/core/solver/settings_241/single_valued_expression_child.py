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
from .average_over import average_over as average_over_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .definition import definition as definition_cls
from .list_valid_report_names import list_valid_report_names as list_valid_report_names_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls
class single_valued_expression_child(Group):
    """
    'child_object_type' of single_valued_expression.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'average_over', 'retain_instantaneous_values', 'definition',
         'list_valid_report_names']

    command_names = \
        ['create_output_parameter']

    _child_classes = dict(
        name=name_cls,
        average_over=average_over_cls,
        retain_instantaneous_values=retain_instantaneous_values_cls,
        definition=definition_cls,
        list_valid_report_names=list_valid_report_names_cls,
        create_output_parameter=create_output_parameter_cls,
    )

