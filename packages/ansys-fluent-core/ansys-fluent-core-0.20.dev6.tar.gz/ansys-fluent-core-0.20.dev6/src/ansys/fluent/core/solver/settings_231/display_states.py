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
from .use_active import use_active as use_active_cls
from .restore_state import restore_state as restore_state_cls
from .copy_4 import copy as copy_cls
from .read_3 import read as read_cls
from .write_1 import write as write_cls
from .display_states_child import display_states_child

class display_states(NamedObject[display_states_child], _CreatableNamedObjectMixin[display_states_child]):
    """
    'display_states' child.
    """

    fluent_name = "display-states"

    command_names = \
        ['list', 'use_active', 'restore_state', 'copy', 'read', 'write']

    _child_classes = dict(
        list=list_cls,
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
