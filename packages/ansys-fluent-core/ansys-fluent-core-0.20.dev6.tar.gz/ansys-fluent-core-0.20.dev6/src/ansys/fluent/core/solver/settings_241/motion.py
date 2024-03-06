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

from .motion_type import motion_type as motion_type_cls
from .constant_velocity import constant_velocity as constant_velocity_cls
from .zone_track import zone_track as zone_track_cls
class motion(Group):
    """
    'motion' child.
    """

    fluent_name = "motion"

    child_names = \
        ['motion_type', 'constant_velocity', 'zone_track']

    _child_classes = dict(
        motion_type=motion_type_cls,
        constant_velocity=constant_velocity_cls,
        zone_track=zone_track_cls,
    )

