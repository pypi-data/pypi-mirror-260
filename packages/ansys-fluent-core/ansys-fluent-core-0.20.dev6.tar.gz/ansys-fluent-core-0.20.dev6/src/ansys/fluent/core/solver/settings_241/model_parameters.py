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

from .electrolyte_submodel_enabled import electrolyte_submodel_enabled as electrolyte_submodel_enabled_cls
from .vol_energy_enabled import vol_energy_enabled as vol_energy_enabled_cls
from .surf_energy_enabled import surf_energy_enabled as surf_energy_enabled_cls
from .species_enabled import species_enabled as species_enabled_cls
from .co_echemistry_disabled import co_echemistry_disabled as co_echemistry_disabled_cls
from .electrolysis_mode_enabled import electrolysis_mode_enabled as electrolysis_mode_enabled_cls
from .knudsen_diff_enabled import knudsen_diff_enabled as knudsen_diff_enabled_cls
from .individual_bc_enabled import individual_bc_enabled as individual_bc_enabled_cls
from .converg_voltage_enabled import converg_voltage_enabled as converg_voltage_enabled_cls
from .system_voltage import system_voltage as system_voltage_cls
from .system_current import system_current as system_current_cls
from .leakage_current_density import leakage_current_density as leakage_current_density_cls
from .electrolyte_thickness_1 import electrolyte_thickness as electrolyte_thickness_cls
from .electrolyte_resistivity import electrolyte_resistivity as electrolyte_resistivity_cls
from .current_urf_1 import current_urf as current_urf_cls
from .fcycle_amg_enabled import fcycle_amg_enabled as fcycle_amg_enabled_cls
class model_parameters(Group):
    """
    Model Parameters.
    """

    fluent_name = "model-parameters"

    child_names = \
        ['electrolyte_submodel_enabled', 'vol_energy_enabled',
         'surf_energy_enabled', 'species_enabled', 'co_echemistry_disabled',
         'electrolysis_mode_enabled', 'knudsen_diff_enabled',
         'individual_bc_enabled', 'converg_voltage_enabled', 'system_voltage',
         'system_current', 'leakage_current_density', 'electrolyte_thickness',
         'electrolyte_resistivity', 'current_urf', 'fcycle_amg_enabled']

    _child_classes = dict(
        electrolyte_submodel_enabled=electrolyte_submodel_enabled_cls,
        vol_energy_enabled=vol_energy_enabled_cls,
        surf_energy_enabled=surf_energy_enabled_cls,
        species_enabled=species_enabled_cls,
        co_echemistry_disabled=co_echemistry_disabled_cls,
        electrolysis_mode_enabled=electrolysis_mode_enabled_cls,
        knudsen_diff_enabled=knudsen_diff_enabled_cls,
        individual_bc_enabled=individual_bc_enabled_cls,
        converg_voltage_enabled=converg_voltage_enabled_cls,
        system_voltage=system_voltage_cls,
        system_current=system_current_cls,
        leakage_current_density=leakage_current_density_cls,
        electrolyte_thickness=electrolyte_thickness_cls,
        electrolyte_resistivity=electrolyte_resistivity_cls,
        current_urf=current_urf_cls,
        fcycle_amg_enabled=fcycle_amg_enabled_cls,
    )

