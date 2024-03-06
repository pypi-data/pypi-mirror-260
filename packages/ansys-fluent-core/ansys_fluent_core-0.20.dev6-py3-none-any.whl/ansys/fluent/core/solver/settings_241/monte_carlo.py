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

from .number_of_histories import number_of_histories as number_of_histories_cls
from .under_relaxation import under_relaxation as under_relaxation_cls
from .target_cells_per_volume_cluster import target_cells_per_volume_cluster as target_cells_per_volume_cluster_cls
class monte_carlo(Group):
    """
    Enable/disable the Monte Carlo radiation model.
    """

    fluent_name = "monte-carlo"

    child_names = \
        ['number_of_histories', 'under_relaxation',
         'target_cells_per_volume_cluster']

    _child_classes = dict(
        number_of_histories=number_of_histories_cls,
        under_relaxation=under_relaxation_cls,
        target_cells_per_volume_cluster=target_cells_per_volume_cluster_cls,
    )

