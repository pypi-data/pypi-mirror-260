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

from .plane_coefficients import plane_coefficients as plane_coefficients_cls
from .distance import distance as distance_cls
from .visible_1 import visible as visible_cls
class mirror_planes_child(Group):
    """
    'child_object_type' of mirror_planes.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['plane_coefficients', 'distance', 'visible']

    _child_classes = dict(
        plane_coefficients=plane_coefficients_cls,
        distance=distance_cls,
        visible=visible_cls,
    )

