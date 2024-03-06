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

from .subspace_size import subspace_size as subspace_size_cls
from .skip_iter_count import skip_iter_count as skip_iter_count_cls
class reduced_rank_extrapolation_options(Group):
    """
    Reduced Rank Extrapolation options.
    """

    fluent_name = "reduced-rank-extrapolation-options"

    child_names = \
        ['subspace_size', 'skip_iter_count']

    _child_classes = dict(
        subspace_size=subspace_size_cls,
        skip_iter_count=skip_iter_count_cls,
    )

