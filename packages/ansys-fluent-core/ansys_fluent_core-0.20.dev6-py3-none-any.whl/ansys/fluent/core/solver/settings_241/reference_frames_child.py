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
from .motion import motion as motion_cls
from .parent_1 import parent_1 as parent_1_cls
from .initial_state import initial_state as initial_state_cls
from .display_state import display_state as display_state_cls
class reference_frames_child(Group):
    """
    'child_object_type' of reference_frames.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'motion', 'parent_1', 'initial_state', 'display_state']

    _child_classes = dict(
        name=name_cls,
        motion=motion_cls,
        parent_1=parent_1_cls,
        initial_state=initial_state_cls,
        display_state=display_state_cls,
    )

