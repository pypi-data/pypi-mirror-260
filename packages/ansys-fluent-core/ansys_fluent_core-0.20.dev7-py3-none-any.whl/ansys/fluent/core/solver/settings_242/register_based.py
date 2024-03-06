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
from .rename import rename as rename_cls
from .list_2 import list as list_cls
from .list_properties_5 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .set_1 import set as set_cls
from .register_based_child import register_based_child

class register_based(NamedObject[register_based_child], _CreatableNamedObjectMixin[register_based_child]):
    """
    Set up the application of poor mesh numerics to cells in a register.
    """

    fluent_name = "register-based"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy', 'set']

    _child_classes = dict(
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        set=set_cls,
    )

    child_object_type: register_based_child = register_based_child
    """
    child_object_type of register_based.
    """
