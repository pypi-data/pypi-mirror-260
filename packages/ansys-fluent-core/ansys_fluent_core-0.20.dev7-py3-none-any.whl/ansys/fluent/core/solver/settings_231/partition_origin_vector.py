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

from .relaxation_factor_child import relaxation_factor_child

class partition_origin_vector(ListObject[relaxation_factor_child]):
    """
    'partition_origin_vector' child.
    """

    fluent_name = "partition-origin-vector"

    child_object_type: relaxation_factor_child = relaxation_factor_child
    """
    child_object_type of partition_origin_vector.
    """
