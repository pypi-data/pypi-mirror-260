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

from .display import display as display_cls
from .particle_tracks_child import particle_tracks_child

class particle_tracks(NamedObject[particle_tracks_child], _CreatableNamedObjectMixin[particle_tracks_child]):
    """
    'particle_tracks' child.
    """

    fluent_name = "particle-tracks"

    command_names = \
        ['display']

    _child_classes = dict(
        display=display_cls,
    )

    child_object_type: particle_tracks_child = particle_tracks_child
    """
    child_object_type of particle_tracks.
    """
