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
from .function_name import function_name as function_name_cls
from .input_params import input_params as input_params_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls
class user_defined_child(Group):
    """
    'child_object_type' of user_defined.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'average_over', 'retain_instantaneous_values',
         'function_name', 'input_params']

    command_names = \
        ['create_output_parameter']

    _child_classes = dict(
        name=name_cls,
        average_over=average_over_cls,
        retain_instantaneous_values=retain_instantaneous_values_cls,
        function_name=function_name_cls,
        input_params=input_params_cls,
        create_output_parameter=create_output_parameter_cls,
    )

