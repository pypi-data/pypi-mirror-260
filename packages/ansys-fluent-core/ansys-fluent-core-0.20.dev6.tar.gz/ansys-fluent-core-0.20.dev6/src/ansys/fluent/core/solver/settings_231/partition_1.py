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

from .auto import auto as auto_cls
from .set_3 import set as set_cls
from .combine_partition import combine_partition as combine_partition_cls
from .merge_clusters import merge_clusters as merge_clusters_cls
from .method_3 import method as method_cls
from .print_partitions import print_partitions as print_partitions_cls
from .print_active_partitions import print_active_partitions as print_active_partitions_cls
from .print_stored_partitions import print_stored_partitions as print_stored_partitions_cls
from .reorder_partitions import reorder_partitions as reorder_partitions_cls
from .reorder_partitions_to_architecture import reorder_partitions_to_architecture as reorder_partitions_to_architecture_cls
from .smooth_partition import smooth_partition as smooth_partition_cls
from .use_stored_partitions import use_stored_partitions as use_stored_partitions_cls
class partition(Group):
    """
    Enter the partition domain menu.
    """

    fluent_name = "partition"

    child_names = \
        ['auto', 'set']

    command_names = \
        ['combine_partition', 'merge_clusters', 'method', 'print_partitions',
         'print_active_partitions', 'print_stored_partitions',
         'reorder_partitions', 'reorder_partitions_to_architecture',
         'smooth_partition', 'use_stored_partitions']

    _child_classes = dict(
        auto=auto_cls,
        set=set_cls,
        combine_partition=combine_partition_cls,
        merge_clusters=merge_clusters_cls,
        method=method_cls,
        print_partitions=print_partitions_cls,
        print_active_partitions=print_active_partitions_cls,
        print_stored_partitions=print_stored_partitions_cls,
        reorder_partitions=reorder_partitions_cls,
        reorder_partitions_to_architecture=reorder_partitions_to_architecture_cls,
        smooth_partition=smooth_partition_cls,
        use_stored_partitions=use_stored_partitions_cls,
    )

