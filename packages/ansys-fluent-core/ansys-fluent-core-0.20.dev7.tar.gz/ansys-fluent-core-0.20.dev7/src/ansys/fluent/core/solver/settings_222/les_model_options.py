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

from .dynamic_stress import dynamic_stress as dynamic_stress_cls
from .dynamic_energy_flux import dynamic_energy_flux as dynamic_energy_flux_cls
from .dynamic_scalar_flux import dynamic_scalar_flux as dynamic_scalar_flux_cls
from .subgrid_dynamic_fvar import subgrid_dynamic_fvar as subgrid_dynamic_fvar_cls
class les_model_options(Group):
    """
    'les_model_options' child.
    """

    fluent_name = "les-model-options"

    child_names = \
        ['dynamic_stress', 'dynamic_energy_flux', 'dynamic_scalar_flux',
         'subgrid_dynamic_fvar']

    _child_classes = dict(
        dynamic_stress=dynamic_stress_cls,
        dynamic_energy_flux=dynamic_energy_flux_cls,
        dynamic_scalar_flux=dynamic_scalar_flux_cls,
        subgrid_dynamic_fvar=subgrid_dynamic_fvar_cls,
    )

