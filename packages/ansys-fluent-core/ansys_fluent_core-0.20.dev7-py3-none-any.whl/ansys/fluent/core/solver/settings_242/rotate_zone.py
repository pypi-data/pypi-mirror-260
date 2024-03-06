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

from .zone_names_2 import zone_names as zone_names_cls
from .rotation_angle import rotation_angle as rotation_angle_cls
from .origin import origin as origin_cls
from .axis import axis as axis_cls
class rotate_zone(Command):
    """
    Rotate nodal coordinates of input cell zones.
    
    Parameters
    ----------
        zone_names : typing.List[str]
            Rotate specified cell zones.
        rotation_angle : real
            'rotation_angle' child.
        origin : typing.List[real]
            'origin' child.
        axis : typing.List[real]
            'axis' child.
    
    """

    fluent_name = "rotate-zone"

    argument_names = \
        ['zone_names', 'rotation_angle', 'origin', 'axis']

    _child_classes = dict(
        zone_names=zone_names_cls,
        rotation_angle=rotation_angle_cls,
        origin=origin_cls,
        axis=axis_cls,
    )

