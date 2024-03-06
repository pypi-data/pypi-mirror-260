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
from .phase_10 import phase as phase_cls
from .interior import interior as interior_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls
class interior_child(Group):
    """
    'child_object_type' of interior.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'interior']

    query_names = \
        ['adjacent_cell_zone', 'shadow_face_zone']

    _child_classes = dict(
        name=name_cls,
        phase=phase_cls,
        interior=interior_cls,
        adjacent_cell_zone=adjacent_cell_zone_cls,
        shadow_face_zone=shadow_face_zone_cls,
    )

