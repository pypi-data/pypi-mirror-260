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
from .create_output_parameter import create_output_parameter as create_output_parameter_cls
class custom_child(Group):
    """
    'child_object_type' of custom.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name']

    command_names = \
        ['create_output_parameter']

    _child_classes = dict(
        name=name_cls,
        create_output_parameter=create_output_parameter_cls,
    )

