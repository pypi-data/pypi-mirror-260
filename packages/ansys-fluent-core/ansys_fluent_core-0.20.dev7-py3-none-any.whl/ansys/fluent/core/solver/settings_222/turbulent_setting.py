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

from .averaged_turbulent_parameters import averaged_turbulent_parameters as averaged_turbulent_parameters_cls
from .turbulent_intensity_1 import turbulent_intensity as turbulent_intensity_cls
from .viscosity_ratio_1 import viscosity_ratio as viscosity_ratio_cls
class turbulent_setting(Group):
    """
    Enter the turbulent settings menu.
    """

    fluent_name = "turbulent-setting"

    child_names = \
        ['averaged_turbulent_parameters', 'turbulent_intensity',
         'viscosity_ratio']

    _child_classes = dict(
        averaged_turbulent_parameters=averaged_turbulent_parameters_cls,
        turbulent_intensity=turbulent_intensity_cls,
        viscosity_ratio=viscosity_ratio_cls,
    )

