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

from .data_reduction_interval import data_reduction_interval as data_reduction_interval_cls
from .target_num_parcels_per_face import target_num_parcels_per_face as target_num_parcels_per_face_cls
class data_reduction(Group):
    """
    Help not available.
    """

    fluent_name = "data-reduction"

    child_names = \
        ['data_reduction_interval', 'target_num_parcels_per_face']

    _child_classes = dict(
        data_reduction_interval=data_reduction_interval_cls,
        target_num_parcels_per_face=target_num_parcels_per_face_cls,
    )

