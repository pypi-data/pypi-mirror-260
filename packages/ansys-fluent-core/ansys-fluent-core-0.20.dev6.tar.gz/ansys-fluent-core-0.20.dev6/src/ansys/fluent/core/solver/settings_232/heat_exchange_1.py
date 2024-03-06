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

from .computed_heat_rejection import computed_heat_rejection as computed_heat_rejection_cls
from .inlet_temperature import inlet_temperature as inlet_temperature_cls
from .outlet_temperature import outlet_temperature as outlet_temperature_cls
from .mass_flow_rate_1 import mass_flow_rate as mass_flow_rate_cls
from .specific_heat_5 import specific_heat as specific_heat_cls
class heat_exchange(Group):
    """
    'heat_exchange' child.
    """

    fluent_name = "heat-exchange"

    command_names = \
        ['computed_heat_rejection', 'inlet_temperature', 'outlet_temperature',
         'mass_flow_rate', 'specific_heat']

    _child_classes = dict(
        computed_heat_rejection=computed_heat_rejection_cls,
        inlet_temperature=inlet_temperature_cls,
        outlet_temperature=outlet_temperature_cls,
        mass_flow_rate=mass_flow_rate_cls,
        specific_heat=specific_heat_cls,
    )

