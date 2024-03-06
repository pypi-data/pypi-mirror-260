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

from .degassing_verbosity import degassing_verbosity as degassing_verbosity_cls
from .mass_flow import mass_flow as mass_flow_cls
from .pressure_outlet_1 import pressure_outlet as pressure_outlet_cls
from .pressure_far_field_1 import pressure_far_field as pressure_far_field_cls
from .physical_velocity_porous_formulation import physical_velocity_porous_formulation as physical_velocity_porous_formulation_cls
from .target_mass_flow_rate_settings import target_mass_flow_rate_settings as target_mass_flow_rate_settings_cls
from .advanced_1 import advanced as advanced_cls
class settings(Group):
    """
    'settings' child.
    """

    fluent_name = "settings"

    child_names = \
        ['degassing_verbosity', 'mass_flow', 'pressure_outlet',
         'pressure_far_field', 'physical_velocity_porous_formulation',
         'target_mass_flow_rate_settings', 'advanced']

    _child_classes = dict(
        degassing_verbosity=degassing_verbosity_cls,
        mass_flow=mass_flow_cls,
        pressure_outlet=pressure_outlet_cls,
        pressure_far_field=pressure_far_field_cls,
        physical_velocity_porous_formulation=physical_velocity_porous_formulation_cls,
        target_mass_flow_rate_settings=target_mass_flow_rate_settings_cls,
        advanced=advanced_cls,
    )

