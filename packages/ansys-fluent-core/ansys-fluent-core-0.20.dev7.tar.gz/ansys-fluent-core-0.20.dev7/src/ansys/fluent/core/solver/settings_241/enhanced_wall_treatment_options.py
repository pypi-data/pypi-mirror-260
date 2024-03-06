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

from .pressure_gradient_effects import pressure_gradient_effects as pressure_gradient_effects_cls
from .thermal_effects import thermal_effects as thermal_effects_cls
class enhanced_wall_treatment_options(Group):
    """
    'enhanced_wall_treatment_options' child.
    """

    fluent_name = "enhanced-wall-treatment-options"

    child_names = \
        ['pressure_gradient_effects', 'thermal_effects']

    _child_classes = dict(
        pressure_gradient_effects=pressure_gradient_effects_cls,
        thermal_effects=thermal_effects_cls,
    )

