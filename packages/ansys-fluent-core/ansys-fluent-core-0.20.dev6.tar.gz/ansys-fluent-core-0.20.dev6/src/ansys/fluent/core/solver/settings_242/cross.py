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

from .option import option as option_cls
from .zero_shear_viscosity import zero_shear_viscosity as zero_shear_viscosity_cls
from .power_law_index import power_law_index as power_law_index_cls
from .time_constant import time_constant as time_constant_cls
from .reference_temperature import reference_temperature as reference_temperature_cls
from .activation_energy import activation_energy as activation_energy_cls
class cross(Group):
    """
    'cross' child.
    """

    fluent_name = "cross"

    child_names = \
        ['option', 'zero_shear_viscosity', 'power_law_index', 'time_constant',
         'reference_temperature', 'activation_energy']

    _child_classes = dict(
        option=option_cls,
        zero_shear_viscosity=zero_shear_viscosity_cls,
        power_law_index=power_law_index_cls,
        time_constant=time_constant_cls,
        reference_temperature=reference_temperature_cls,
        activation_energy=activation_energy_cls,
    )

