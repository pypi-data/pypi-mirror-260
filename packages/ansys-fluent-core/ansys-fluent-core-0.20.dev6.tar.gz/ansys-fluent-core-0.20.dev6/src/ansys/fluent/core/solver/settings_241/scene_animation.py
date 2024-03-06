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

from .set_custom_frames_1 import set_custom_frames as set_custom_frames_cls
from .read_animation import read_animation as read_animation_cls
from .write_animation_1 import write_animation as write_animation_cls
from .add_keyframe import add_keyframe as add_keyframe_cls
from .delete_keyframe import delete_keyframe as delete_keyframe_cls
from .delete_all_keyframes import delete_all_keyframes as delete_all_keyframes_cls
from .play_1 import play as play_cls
class scene_animation(Group):
    """
    Keyframe animation option menu.
    """

    fluent_name = "scene-animation"

    child_names = \
        ['set_custom_frames']

    command_names = \
        ['read_animation', 'write_animation', 'add_keyframe',
         'delete_keyframe', 'delete_all_keyframes', 'play']

    _child_classes = dict(
        set_custom_frames=set_custom_frames_cls,
        read_animation=read_animation_cls,
        write_animation=write_animation_cls,
        add_keyframe=add_keyframe_cls,
        delete_keyframe=delete_keyframe_cls,
        delete_all_keyframes=delete_all_keyframes_cls,
        play=play_cls,
    )

