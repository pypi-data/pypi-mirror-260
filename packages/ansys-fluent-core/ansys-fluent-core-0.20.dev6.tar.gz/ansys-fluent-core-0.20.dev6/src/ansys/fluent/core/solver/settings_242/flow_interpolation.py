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

from .specific_heat_enabled import specific_heat_enabled as specific_heat_enabled_cls
from .density_enabled import density_enabled as density_enabled_cls
from .gradients_enabled import gradients_enabled as gradients_enabled_cls
from .viscosity_enabled import viscosity_enabled as viscosity_enabled_cls
from .temperature_enabled import temperature_enabled as temperature_enabled_cls
from .wall_zero_vel_enabled import wall_zero_vel_enabled as wall_zero_vel_enabled_cls
class flow_interpolation(Group):
    """
    Main menu holding options to enable/disable interpolation of flow data to the particle position.
    """

    fluent_name = "flow-interpolation"

    child_names = \
        ['specific_heat_enabled', 'density_enabled', 'gradients_enabled',
         'viscosity_enabled', 'temperature_enabled', 'wall_zero_vel_enabled']

    _child_classes = dict(
        specific_heat_enabled=specific_heat_enabled_cls,
        density_enabled=density_enabled_cls,
        gradients_enabled=gradients_enabled_cls,
        viscosity_enabled=viscosity_enabled_cls,
        temperature_enabled=temperature_enabled_cls,
        wall_zero_vel_enabled=wall_zero_vel_enabled_cls,
    )

