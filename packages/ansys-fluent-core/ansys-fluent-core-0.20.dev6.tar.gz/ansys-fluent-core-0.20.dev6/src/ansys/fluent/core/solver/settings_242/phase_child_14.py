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

from .network_end import network_end as network_end_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['network_end']

    query_names = \
        ['adjacent_cell_zone', 'shadow_face_zone']

    _child_classes = dict(
        network_end=network_end_cls,
        adjacent_cell_zone=adjacent_cell_zone_cls,
        shadow_face_zone=shadow_face_zone_cls,
    )

