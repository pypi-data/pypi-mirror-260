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

from .delete_1 import delete as delete_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .set_damping_strengths_child import set_damping_strengths_child

class input_parameters(NamedObject[set_damping_strengths_child], _NonCreatableNamedObjectMixin[set_damping_strengths_child]):
    """
    Input Parameter Values of Design Point.
    """

    fluent_name = "input-parameters"

    command_names = \
        ['delete', 'list', 'list_properties', 'make_a_copy']

    _child_classes = dict(
        delete=delete_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
    )

    child_object_type: set_damping_strengths_child = set_damping_strengths_child
    """
    child_object_type of input_parameters.
    """
