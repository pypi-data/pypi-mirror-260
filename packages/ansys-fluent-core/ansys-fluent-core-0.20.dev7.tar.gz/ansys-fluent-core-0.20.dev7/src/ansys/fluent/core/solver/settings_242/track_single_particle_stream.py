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

from .enabled_40 import enabled as enabled_cls
from .stream_id import stream_id as stream_id_cls
class track_single_particle_stream(Group):
    """
    Enable track single particle stream.
    """

    fluent_name = "track-single-particle-stream"

    child_names = \
        ['enabled', 'stream_id']

    _child_classes = dict(
        enabled=enabled_cls,
        stream_id=stream_id_cls,
    )

