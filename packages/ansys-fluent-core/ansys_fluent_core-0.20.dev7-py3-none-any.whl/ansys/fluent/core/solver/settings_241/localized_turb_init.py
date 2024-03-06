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

from .enabled_16 import enabled as enabled_cls
from .turbulent_intensity_2 import turbulent_intensity as turbulent_intensity_cls
from .turbulent_viscosity_ratio_2 import turbulent_viscosity_ratio as turbulent_viscosity_ratio_cls
class localized_turb_init(Group):
    """
    Localized initialization of turbulent flow variables for VOF/Mixture multiphase flow models.
    """

    fluent_name = "localized-turb-init"

    child_names = \
        ['enabled', 'turbulent_intensity', 'turbulent_viscosity_ratio']

    _child_classes = dict(
        enabled=enabled_cls,
        turbulent_intensity=turbulent_intensity_cls,
        turbulent_viscosity_ratio=turbulent_viscosity_ratio_cls,
    )

