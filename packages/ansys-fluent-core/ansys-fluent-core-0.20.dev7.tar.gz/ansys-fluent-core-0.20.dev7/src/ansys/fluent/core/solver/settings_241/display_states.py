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
from .list_3 import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .use_active import use_active as use_active_cls
from .restore_state import restore_state as restore_state_cls
from .copy_5 import copy as copy_cls
from .read_3 import read as read_cls
from .write_1 import write as write_cls
from .display_states_child import display_states_child

class display_states(NamedObject[display_states_child], _CreatableNamedObjectMixin[display_states_child]):
    """
    'display_states' child.
    """

    fluent_name = "display-states"

    command_names = \
        ['delete', 'list', 'list_properties', 'make_a_copy', 'use_active',
         'restore_state', 'copy', 'read', 'write']

    _child_classes = dict(
        delete=delete_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        use_active=use_active_cls,
        restore_state=restore_state_cls,
        copy=copy_cls,
        read=read_cls,
        write=write_cls,
    )

    child_object_type: display_states_child = display_states_child
    """
    child_object_type of display_states.
    """
