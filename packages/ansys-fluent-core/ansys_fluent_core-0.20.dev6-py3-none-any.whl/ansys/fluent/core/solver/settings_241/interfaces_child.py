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

from .name import name as name_cls
from .type_6 import type as type_cls
from .boundary_1 import boundary_1 as boundary_1_cls
from .boundary_2 import boundary_2 as boundary_2_cls
from .periodicity import periodicity as periodicity_cls
from .mesh_connectivity import mesh_connectivity as mesh_connectivity_cls
class interfaces_child(Group):
    """
    'child_object_type' of interfaces.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'type', 'boundary_1', 'boundary_2', 'periodicity',
         'mesh_connectivity']

    _child_classes = dict(
        name=name_cls,
        type=type_cls,
        boundary_1=boundary_1_cls,
        boundary_2=boundary_2_cls,
        periodicity=periodicity_cls,
        mesh_connectivity=mesh_connectivity_cls,
    )

