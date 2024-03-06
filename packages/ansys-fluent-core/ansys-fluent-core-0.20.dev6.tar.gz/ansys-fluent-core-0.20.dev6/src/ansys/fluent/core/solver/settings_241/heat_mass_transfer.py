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

from .cavitation import cavitation as cavitation_cls
from .evaporation_condensation import evaporation_condensation as evaporation_condensation_cls
from .boiling import boiling as boiling_cls
from .area_density_1 import area_density as area_density_cls
from .alternative_energy_treatment import alternative_energy_treatment as alternative_energy_treatment_cls
class heat_mass_transfer(Group):
    """
    Multiphase interphase heat and mass transfer numerics options menu.
    """

    fluent_name = "heat-mass-transfer"

    child_names = \
        ['cavitation', 'evaporation_condensation', 'boiling', 'area_density',
         'alternative_energy_treatment']

    _child_classes = dict(
        cavitation=cavitation_cls,
        evaporation_condensation=evaporation_condensation_cls,
        boiling=boiling_cls,
        area_density=area_density_cls,
        alternative_energy_treatment=alternative_energy_treatment_cls,
    )

