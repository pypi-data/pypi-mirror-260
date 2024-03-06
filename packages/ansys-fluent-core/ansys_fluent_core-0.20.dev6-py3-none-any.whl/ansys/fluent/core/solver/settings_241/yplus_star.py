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

from .option_11 import option as option_cls
from .min_allowed import min_allowed as min_allowed_cls
from .max_allowed import max_allowed as max_allowed_cls
from .wall_zones import wall_zones as wall_zones_cls
from .phase_28 import phase as phase_cls
class yplus_star(Group):
    """
    'yplus_star' child.
    """

    fluent_name = "yplus-star"

    child_names = \
        ['option', 'min_allowed', 'max_allowed', 'wall_zones', 'phase']

    _child_classes = dict(
        option=option_cls,
        min_allowed=min_allowed_cls,
        max_allowed=max_allowed_cls,
        wall_zones=wall_zones_cls,
        phase=phase_cls,
    )

