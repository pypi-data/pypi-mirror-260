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

from .enable_mesh_interface_clustering import enable_mesh_interface_clustering as enable_mesh_interface_clustering_cls
from .split_angle import split_angle as split_angle_cls
from .clustering_algorithm import clustering_algorithm as clustering_algorithm_cls
from .enable_clustering import enable_clustering as enable_clustering_cls
from .faces_per_cluster import faces_per_cluster as faces_per_cluster_cls
from .print_thread_clusters import print_thread_clusters as print_thread_clusters_cls
class clustering_settings(Group):
    """
    Enter clustering related settings.
    """

    fluent_name = "clustering-settings"

    child_names = \
        ['enable_mesh_interface_clustering', 'split_angle',
         'clustering_algorithm', 'enable_clustering', 'faces_per_cluster']

    command_names = \
        ['print_thread_clusters']

    _child_classes = dict(
        enable_mesh_interface_clustering=enable_mesh_interface_clustering_cls,
        split_angle=split_angle_cls,
        clustering_algorithm=clustering_algorithm_cls,
        enable_clustering=enable_clustering_cls,
        faces_per_cluster=faces_per_cluster_cls,
        print_thread_clusters=print_thread_clusters_cls,
    )

