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

from .enable_4 import enable as enable_cls
from .zone_name_5 import zone_name as zone_name_cls
class inlet_temperature_for_operating_density(Group):
    """
    Enable/disable non-zero operating density computed from inlet temperature.
    """

    fluent_name = "inlet-temperature-for-operating-density"

    child_names = \
        ['enable', 'zone_name']

    _child_classes = dict(
        enable=enable_cls,
        zone_name=zone_name_cls,
    )

