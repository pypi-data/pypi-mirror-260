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

from .option_3 import option as option_cls
from .consistency_index import consistency_index as consistency_index_cls
from .power_law_index import power_law_index as power_law_index_cls
from .minimum_viscosity import minimum_viscosity as minimum_viscosity_cls
from .maximum_viscosity import maximum_viscosity as maximum_viscosity_cls
from .reference_temperature import reference_temperature as reference_temperature_cls
from .activation_energy import activation_energy as activation_energy_cls
class non_newtonian_power_law(Group):
    """
    'non_newtonian_power_law' child.
    """

    fluent_name = "non-newtonian-power-law"

    child_names = \
        ['option', 'consistency_index', 'power_law_index',
         'minimum_viscosity', 'maximum_viscosity', 'reference_temperature',
         'activation_energy']

    _child_classes = dict(
        option=option_cls,
        consistency_index=consistency_index_cls,
        power_law_index=power_law_index_cls,
        minimum_viscosity=minimum_viscosity_cls,
        maximum_viscosity=maximum_viscosity_cls,
        reference_temperature=reference_temperature_cls,
        activation_energy=activation_energy_cls,
    )

