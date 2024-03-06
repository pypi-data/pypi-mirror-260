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

from .x import x as x_cls
from .x_2 import x_2 as x_2_cls
from .y import y as y_cls
from .y_2 import y_2 as y_2_cls
from .z import z as z_cls
from .z_2 import z_2 as z_2_cls
from .azimuthal_start_angle import azimuthal_start_angle as azimuthal_start_angle_cls
from .azimuthal_stop_angle import azimuthal_stop_angle as azimuthal_stop_angle_cls
from .injection_surfaces import injection_surfaces as injection_surfaces_cls
from .random_surface_inj import random_surface_inj as random_surface_inj_cls
class location(Group):
    """
    'location' child.
    """

    fluent_name = "location"

    child_names = \
        ['x', 'x_2', 'y', 'y_2', 'z', 'z_2', 'azimuthal_start_angle',
         'azimuthal_stop_angle', 'injection_surfaces', 'random_surface_inj']

    _child_classes = dict(
        x=x_cls,
        x_2=x_2_cls,
        y=y_cls,
        y_2=y_2_cls,
        z=z_cls,
        z_2=z_2_cls,
        azimuthal_start_angle=azimuthal_start_angle_cls,
        azimuthal_stop_angle=azimuthal_stop_angle_cls,
        injection_surfaces=injection_surfaces_cls,
        random_surface_inj=random_surface_inj_cls,
    )

