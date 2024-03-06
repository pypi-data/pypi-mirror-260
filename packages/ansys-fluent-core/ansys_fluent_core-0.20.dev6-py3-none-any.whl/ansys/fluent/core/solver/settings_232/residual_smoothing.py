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

from .residual_smoothing_factor import residual_smoothing_factor as residual_smoothing_factor_cls
from .residual_smoothing_iter_count import residual_smoothing_iter_count as residual_smoothing_iter_count_cls
class residual_smoothing(Group):
    """
    Set residual smoothing factor and number of iterations.
    """

    fluent_name = "residual-smoothing"

    child_names = \
        ['residual_smoothing_factor', 'residual_smoothing_iter_count']

    _child_classes = dict(
        residual_smoothing_factor=residual_smoothing_factor_cls,
        residual_smoothing_iter_count=residual_smoothing_iter_count_cls,
    )

