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

from .player import player as player_cls
from .start_frame_1 import start_frame as start_frame_cls
from .end_frame_1 import end_frame as end_frame_cls
from .increment_1 import increment as increment_cls
from .playback_mode import playback_mode as playback_mode_cls
from .speed_1 import speed as speed_cls
class play(Command):
    """
    Play the selected animation.
    
    Parameters
    ----------
        player : str
            Enter the Player Operation.
        start_frame : int
            Start Frame Number.
        end_frame : int
            Start Frame Number.
        increment : int
            Skip frame while playing.
        playback_mode : str
            Enter the playback mode.
        speed : int
            Animation play speed.
    
    """

    fluent_name = "play"

    argument_names = \
        ['player', 'start_frame', 'end_frame', 'increment', 'playback_mode',
         'speed']

    _child_classes = dict(
        player=player_cls,
        start_frame=start_frame_cls,
        end_frame=end_frame_cls,
        increment=increment_cls,
        playback_mode=playback_mode_cls,
        speed=speed_cls,
    )

