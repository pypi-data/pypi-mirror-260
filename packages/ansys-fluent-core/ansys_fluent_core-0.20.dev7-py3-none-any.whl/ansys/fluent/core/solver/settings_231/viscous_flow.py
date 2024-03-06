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

from .viscosity_averaging import viscosity_averaging as viscosity_averaging_cls
from .turb_visc_based_damping import turb_visc_based_damping as turb_visc_based_damping_cls
from .density_func_expo import density_func_expo as density_func_expo_cls
from .density_ratio_cutoff import density_ratio_cutoff as density_ratio_cutoff_cls
from .interfacial_artificial_viscosity import interfacial_artificial_viscosity as interfacial_artificial_viscosity_cls
class viscous_flow(Group):
    """
    Multiphase viscous flow numerics options menu.
    """

    fluent_name = "viscous-flow"

    child_names = \
        ['viscosity_averaging', 'turb_visc_based_damping',
         'density_func_expo', 'density_ratio_cutoff',
         'interfacial_artificial_viscosity']

    _child_classes = dict(
        viscosity_averaging=viscosity_averaging_cls,
        turb_visc_based_damping=turb_visc_based_damping_cls,
        density_func_expo=density_func_expo_cls,
        density_ratio_cutoff=density_ratio_cutoff_cls,
        interfacial_artificial_viscosity=interfacial_artificial_viscosity_cls,
    )

