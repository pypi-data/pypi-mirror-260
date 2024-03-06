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

from .allow_repair_at_boundaries import allow_repair_at_boundaries as allow_repair_at_boundaries_cls
from .include_local_polyhedra_conversion_in_repair import include_local_polyhedra_conversion_in_repair as include_local_polyhedra_conversion_in_repair_cls
from .repair_poor_elements import repair_poor_elements as repair_poor_elements_cls
from .improve_quality import improve_quality as improve_quality_cls
from .repair import repair as repair_cls
from .repair_face_handedness import repair_face_handedness as repair_face_handedness_cls
from .repair_face_node_order import repair_face_node_order as repair_face_node_order_cls
from .repair_wall_distance import repair_wall_distance as repair_wall_distance_cls
from .repair_periodic_1 import repair_periodic as repair_periodic_cls
class repair_improve(Group):
    """
    Enter the repair and improve quality menu.
    """

    fluent_name = "repair-improve"

    child_names = \
        ['allow_repair_at_boundaries',
         'include_local_polyhedra_conversion_in_repair']

    command_names = \
        ['repair_poor_elements', 'improve_quality', 'repair',
         'repair_face_handedness', 'repair_face_node_order',
         'repair_wall_distance', 'repair_periodic']

    _child_classes = dict(
        allow_repair_at_boundaries=allow_repair_at_boundaries_cls,
        include_local_polyhedra_conversion_in_repair=include_local_polyhedra_conversion_in_repair_cls,
        repair_poor_elements=repair_poor_elements_cls,
        improve_quality=improve_quality_cls,
        repair=repair_cls,
        repair_face_handedness=repair_face_handedness_cls,
        repair_face_node_order=repair_face_node_order_cls,
        repair_wall_distance=repair_wall_distance_cls,
        repair_periodic=repair_periodic_cls,
    )

