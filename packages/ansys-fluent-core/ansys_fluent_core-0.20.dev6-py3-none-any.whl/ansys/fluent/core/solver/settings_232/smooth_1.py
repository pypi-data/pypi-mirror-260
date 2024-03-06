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

from .smooth_partitioning import smooth_partitioning as smooth_partitioning_cls
from .max_smoothing_iterations import max_smoothing_iterations as max_smoothing_iterations_cls
class smooth(Group):
    """
    Set partition smoothing optimization.
    """

    fluent_name = "smooth"

    child_names = \
        ['smooth_partitioning', 'max_smoothing_iterations']

    _child_classes = dict(
        smooth_partitioning=smooth_partitioning_cls,
        max_smoothing_iterations=max_smoothing_iterations_cls,
    )

