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

from .scale_residuals import scale_residuals as scale_residuals_cls
from .compute_local_scale import compute_local_scale as compute_local_scale_cls
from .reporting_option import reporting_option as reporting_option_cls
class residual_values(Group):
    """
    Enable/disable scaling of residuals by coefficient sum in printed and plotted output.
    """

    fluent_name = "residual-values"

    child_names = \
        ['scale_residuals', 'compute_local_scale', 'reporting_option']

    _child_classes = dict(
        scale_residuals=scale_residuals_cls,
        compute_local_scale=compute_local_scale_cls,
        reporting_option=reporting_option_cls,
    )

    _child_aliases = dict(
        scale_type="reporting_option",
    )

