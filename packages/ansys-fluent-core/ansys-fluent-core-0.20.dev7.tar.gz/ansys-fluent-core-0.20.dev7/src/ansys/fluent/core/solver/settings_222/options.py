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

from .viscous_heating import viscous_heating as viscous_heating_cls
from .low_pressure_slip import low_pressure_slip as low_pressure_slip_cls
from .curvature_correction import curvature_correction as curvature_correction_cls
from .corner_flow_correction import corner_flow_correction as corner_flow_correction_cls
from .production_kato_launder import production_kato_launder as production_kato_launder_cls
from .production_limiter import production_limiter as production_limiter_cls
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['viscous_heating', 'low_pressure_slip', 'curvature_correction',
         'corner_flow_correction', 'production_kato_launder',
         'production_limiter']

    _child_classes = dict(
        viscous_heating=viscous_heating_cls,
        low_pressure_slip=low_pressure_slip_cls,
        curvature_correction=curvature_correction_cls,
        corner_flow_correction=corner_flow_correction_cls,
        production_kato_launder=production_kato_launder_cls,
        production_limiter=production_limiter_cls,
    )

