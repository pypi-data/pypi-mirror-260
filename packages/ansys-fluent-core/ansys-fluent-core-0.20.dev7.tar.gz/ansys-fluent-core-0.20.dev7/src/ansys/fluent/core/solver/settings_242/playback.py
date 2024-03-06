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

from .set_custom_frames import set_custom_frames as set_custom_frames_cls
from .video_1 import video as video_cls
from .current_animation import current_animation as current_animation_cls
from .read_animation_file import read_animation_file as read_animation_file_cls
from .write_animation import write_animation as write_animation_cls
from .stored_view import stored_view as stored_view_cls
from .delete_5 import delete as delete_cls
from .play import play as play_cls
class playback(Group):
    """
    'playback' child.
    """

    fluent_name = "playback"

    child_names = \
        ['set_custom_frames', 'video', 'current_animation']

    command_names = \
        ['read_animation_file', 'write_animation', 'stored_view', 'delete',
         'play']

    _child_classes = dict(
        set_custom_frames=set_custom_frames_cls,
        video=video_cls,
        current_animation=current_animation_cls,
        read_animation_file=read_animation_file_cls,
        write_animation=write_animation_cls,
        stored_view=stored_view_cls,
        delete=delete_cls,
        play=play_cls,
    )

