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
from .clustering_type import clustering_type as clustering_type_cls
from .nx import nx as nx_cls
from .ny import ny as ny_cls
from .nz import nz as nz_cls
from .cluster_number import cluster_number as cluster_number_cls
from .target_variable import target_variable as target_variable_cls
from .udf_name_1 import udf_name as udf_name_cls
class cell_clustering(Group):
    """
    Set cell clustering information.
    """

    fluent_name = "cell-clustering"

    child_names = \
        ['enabled', 'clustering_type', 'nx', 'ny', 'nz', 'cluster_number',
         'target_variable', 'udf_name']

    _child_classes = dict(
        enabled=enabled_cls,
        clustering_type=clustering_type_cls,
        nx=nx_cls,
        ny=ny_cls,
        nz=nz_cls,
        cluster_number=cluster_number_cls,
        target_variable=target_variable_cls,
        udf_name=udf_name_cls,
    )

