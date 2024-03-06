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

from .chemistry_iterations import chemistry_iterations as chemistry_iterations_cls
from .aggresiveness_factor import aggresiveness_factor as aggresiveness_factor_cls
from .transport_time_scale_factor import transport_time_scale_factor as transport_time_scale_factor_cls
from .min_temperature import min_temperature as min_temperature_cls
class turb_chem_interaction_model_options(Group):
    """
    'turb_chem_interaction_model_options' child.
    """

    fluent_name = "turb-chem-interaction-model-options"

    child_names = \
        ['chemistry_iterations', 'aggresiveness_factor',
         'transport_time_scale_factor', 'min_temperature']

    _child_classes = dict(
        chemistry_iterations=chemistry_iterations_cls,
        aggresiveness_factor=aggresiveness_factor_cls,
        transport_time_scale_factor=transport_time_scale_factor_cls,
        min_temperature=min_temperature_cls,
    )

