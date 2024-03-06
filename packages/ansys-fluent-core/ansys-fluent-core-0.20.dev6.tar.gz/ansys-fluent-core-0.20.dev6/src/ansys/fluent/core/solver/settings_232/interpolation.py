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

from .flow_cp_interpolation_enabled import flow_cp_interpolation_enabled as flow_cp_interpolation_enabled_cls
from .flow_density_interpolation_enabled import flow_density_interpolation_enabled as flow_density_interpolation_enabled_cls
from .flow_gradient_interpolation_enabled import flow_gradient_interpolation_enabled as flow_gradient_interpolation_enabled_cls
from .flow_viscosity_interpolation_enabled import flow_viscosity_interpolation_enabled as flow_viscosity_interpolation_enabled_cls
from .flow_temperature_interpolation_enabled import flow_temperature_interpolation_enabled as flow_temperature_interpolation_enabled_cls
from .zero_nodal_velocities_on_walls import zero_nodal_velocities_on_walls as zero_nodal_velocities_on_walls_cls
class interpolation(Group):
    """
    Main menu holding options to enable/disable interpolation of flow data to the particle position.
    """

    fluent_name = "interpolation"

    child_names = \
        ['flow_cp_interpolation_enabled',
         'flow_density_interpolation_enabled',
         'flow_gradient_interpolation_enabled',
         'flow_viscosity_interpolation_enabled',
         'flow_temperature_interpolation_enabled',
         'zero_nodal_velocities_on_walls']

    _child_classes = dict(
        flow_cp_interpolation_enabled=flow_cp_interpolation_enabled_cls,
        flow_density_interpolation_enabled=flow_density_interpolation_enabled_cls,
        flow_gradient_interpolation_enabled=flow_gradient_interpolation_enabled_cls,
        flow_viscosity_interpolation_enabled=flow_viscosity_interpolation_enabled_cls,
        flow_temperature_interpolation_enabled=flow_temperature_interpolation_enabled_cls,
        zero_nodal_velocities_on_walls=zero_nodal_velocities_on_walls_cls,
    )

