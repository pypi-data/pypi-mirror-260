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

from .potential_boundary_condition import potential_boundary_condition as potential_boundary_condition_cls
from .potential_boundary_value import potential_boundary_value as potential_boundary_value_cls
from .elec_potential_jump import elec_potential_jump as elec_potential_jump_cls
from .elec_potential_resistance import elec_potential_resistance as elec_potential_resistance_cls
from .electrolyte_potential_boundary_condition import electrolyte_potential_boundary_condition as electrolyte_potential_boundary_condition_cls
from .current_density_boundary_value import current_density_boundary_value as current_density_boundary_value_cls
from .echem_reaction import echem_reaction as echem_reaction_cls
from .elec_potential_mechs import elec_potential_mechs as elec_potential_mechs_cls
from .faradaic_heat import faradaic_heat as faradaic_heat_cls
from .li_ion_type import li_ion_type as li_ion_type_cls
from .li_ion_value import li_ion_value as li_ion_value_cls
class potential(Group):
    """
    Help not available.
    """

    fluent_name = "potential"

    child_names = \
        ['potential_boundary_condition', 'potential_boundary_value',
         'elec_potential_jump', 'elec_potential_resistance',
         'electrolyte_potential_boundary_condition',
         'current_density_boundary_value', 'echem_reaction',
         'elec_potential_mechs', 'faradaic_heat', 'li_ion_type',
         'li_ion_value']

    _child_classes = dict(
        potential_boundary_condition=potential_boundary_condition_cls,
        potential_boundary_value=potential_boundary_value_cls,
        elec_potential_jump=elec_potential_jump_cls,
        elec_potential_resistance=elec_potential_resistance_cls,
        electrolyte_potential_boundary_condition=electrolyte_potential_boundary_condition_cls,
        current_density_boundary_value=current_density_boundary_value_cls,
        echem_reaction=echem_reaction_cls,
        elec_potential_mechs=elec_potential_mechs_cls,
        faradaic_heat=faradaic_heat_cls,
        li_ion_type=li_ion_type_cls,
        li_ion_value=li_ion_value_cls,
    )

