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

from .x_velocity import x_velocity as x_velocity_cls
from .x_velocity_2 import x_velocity_2 as x_velocity_2_cls
from .y_velocity import y_velocity as y_velocity_cls
from .y_velocity_2 import y_velocity_2 as y_velocity_2_cls
from .z_velocity import z_velocity as z_velocity_cls
from .z_velocity_2 import z_velocity_2 as z_velocity_2_cls
from .magnitude import magnitude as magnitude_cls
from .swirl_fraction import swirl_fraction as swirl_fraction_cls
from .use_face_normal_direction import use_face_normal_direction as use_face_normal_direction_cls
class velocity(Group):
    """
    'velocity' child.
    """

    fluent_name = "velocity"

    child_names = \
        ['x_velocity', 'x_velocity_2', 'y_velocity', 'y_velocity_2',
         'z_velocity', 'z_velocity_2', 'magnitude', 'swirl_fraction',
         'use_face_normal_direction']

    _child_classes = dict(
        x_velocity=x_velocity_cls,
        x_velocity_2=x_velocity_2_cls,
        y_velocity=y_velocity_cls,
        y_velocity_2=y_velocity_2_cls,
        z_velocity=z_velocity_cls,
        z_velocity_2=z_velocity_2_cls,
        magnitude=magnitude_cls,
        swirl_fraction=swirl_fraction_cls,
        use_face_normal_direction=use_face_normal_direction_cls,
    )

