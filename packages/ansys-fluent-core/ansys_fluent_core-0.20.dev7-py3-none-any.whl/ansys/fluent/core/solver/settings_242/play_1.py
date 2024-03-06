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

from .start_keyframe import start_keyframe as start_keyframe_cls
from .end_keyframe import end_keyframe as end_keyframe_cls
from .increment_2 import increment as increment_cls
class play(Command):
    """
    Play keyframe animation.
    
    Parameters
    ----------
        start_keyframe : int
            Set start keyframe.
        end_keyframe : int
            Set end keyframe.
        increment : int
            Set increment.
    
    """

    fluent_name = "play"

    argument_names = \
        ['start_keyframe', 'end_keyframe', 'increment']

    _child_classes = dict(
        start_keyframe=start_keyframe_cls,
        end_keyframe=end_keyframe_cls,
        increment=increment_cls,
    )

