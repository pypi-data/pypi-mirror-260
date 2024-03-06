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

from .turbulent_specification import turbulent_specification as turbulent_specification_cls
from .modified_turbulent_viscosity import modified_turbulent_viscosity as modified_turbulent_viscosity_cls
from .laminar_kinetic_energy import laminar_kinetic_energy as laminar_kinetic_energy_cls
from .intermittency import intermittency as intermittency_cls
from .turbulent_kinetic_energy import turbulent_kinetic_energy as turbulent_kinetic_energy_cls
from .turbulent_dissipation_rate import turbulent_dissipation_rate as turbulent_dissipation_rate_cls
from .specific_dissipation_rate import specific_dissipation_rate as specific_dissipation_rate_cls
from .velocity_variance_scale import velocity_variance_scale as velocity_variance_scale_cls
from .turbulent_intensity import turbulent_intensity as turbulent_intensity_cls
from .turbulent_length_scale import turbulent_length_scale as turbulent_length_scale_cls
from .hydraulic_diameter import hydraulic_diameter as hydraulic_diameter_cls
from .turbulent_viscosity_ratio import turbulent_viscosity_ratio as turbulent_viscosity_ratio_cls
from .turbulent_viscosity_ratio_profile import turbulent_viscosity_ratio_profile as turbulent_viscosity_ratio_profile_cls
from .reynolds_stress_specification import reynolds_stress_specification as reynolds_stress_specification_cls
from .uu_reynolds_stresses import uu_reynolds_stresses as uu_reynolds_stresses_cls
from .vv_reynolds_stresses import vv_reynolds_stresses as vv_reynolds_stresses_cls
from .ww_reynolds_stresses import ww_reynolds_stresses as ww_reynolds_stresses_cls
from .uv_reynolds_stresses import uv_reynolds_stresses as uv_reynolds_stresses_cls
from .vw_reynolds_stresses import vw_reynolds_stresses as vw_reynolds_stresses_cls
from .uw_reynolds_stresses import uw_reynolds_stresses as uw_reynolds_stresses_cls
from .subgrid_kinetic_energy_specification import subgrid_kinetic_energy_specification as subgrid_kinetic_energy_specification_cls
from .subgrid_kinetic_energy import subgrid_kinetic_energy as subgrid_kinetic_energy_cls
from .subgrid_turbulent_intensity import subgrid_turbulent_intensity as subgrid_turbulent_intensity_cls
class turbulence(Group):
    """
    Help not available.
    """

    fluent_name = "turbulence"

    child_names = \
        ['turbulent_specification', 'modified_turbulent_viscosity',
         'laminar_kinetic_energy', 'intermittency',
         'turbulent_kinetic_energy', 'turbulent_dissipation_rate',
         'specific_dissipation_rate', 'velocity_variance_scale',
         'turbulent_intensity', 'turbulent_length_scale',
         'hydraulic_diameter', 'turbulent_viscosity_ratio',
         'turbulent_viscosity_ratio_profile', 'reynolds_stress_specification',
         'uu_reynolds_stresses', 'vv_reynolds_stresses',
         'ww_reynolds_stresses', 'uv_reynolds_stresses',
         'vw_reynolds_stresses', 'uw_reynolds_stresses',
         'subgrid_kinetic_energy_specification', 'subgrid_kinetic_energy',
         'subgrid_turbulent_intensity']

    _child_classes = dict(
        turbulent_specification=turbulent_specification_cls,
        modified_turbulent_viscosity=modified_turbulent_viscosity_cls,
        laminar_kinetic_energy=laminar_kinetic_energy_cls,
        intermittency=intermittency_cls,
        turbulent_kinetic_energy=turbulent_kinetic_energy_cls,
        turbulent_dissipation_rate=turbulent_dissipation_rate_cls,
        specific_dissipation_rate=specific_dissipation_rate_cls,
        velocity_variance_scale=velocity_variance_scale_cls,
        turbulent_intensity=turbulent_intensity_cls,
        turbulent_length_scale=turbulent_length_scale_cls,
        hydraulic_diameter=hydraulic_diameter_cls,
        turbulent_viscosity_ratio=turbulent_viscosity_ratio_cls,
        turbulent_viscosity_ratio_profile=turbulent_viscosity_ratio_profile_cls,
        reynolds_stress_specification=reynolds_stress_specification_cls,
        uu_reynolds_stresses=uu_reynolds_stresses_cls,
        vv_reynolds_stresses=vv_reynolds_stresses_cls,
        ww_reynolds_stresses=ww_reynolds_stresses_cls,
        uv_reynolds_stresses=uv_reynolds_stresses_cls,
        vw_reynolds_stresses=vw_reynolds_stresses_cls,
        uw_reynolds_stresses=uw_reynolds_stresses_cls,
        subgrid_kinetic_energy_specification=subgrid_kinetic_energy_specification_cls,
        subgrid_kinetic_energy=subgrid_kinetic_energy_cls,
        subgrid_turbulent_intensity=subgrid_turbulent_intensity_cls,
    )

