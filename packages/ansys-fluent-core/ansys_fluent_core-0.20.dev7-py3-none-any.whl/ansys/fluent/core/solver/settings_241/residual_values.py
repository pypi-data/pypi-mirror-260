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
from .scale_type import scale_type as scale_type_cls
class residual_values(Group):
    """
    Enable/disable scaling of residuals by coefficient sum in printed and plotted output.
    """

    fluent_name = "residual-values"

    child_names = \
        ['scale_residuals', 'compute_local_scale', 'scale_type']

    _child_classes = dict(
        scale_residuals=scale_residuals_cls,
        compute_local_scale=compute_local_scale_cls,
        scale_type=scale_type_cls,
    )

