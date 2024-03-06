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

from .point1 import point1 as point1_cls
from .point2_or_vector import point2_or_vector as point2_or_vector_cls
from .diameter_1 import diameter as diameter_cls
class injection_hole_child(Group):
    """
    'child_object_type' of injection_hole.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['point1', 'point2_or_vector', 'diameter']

    _child_classes = dict(
        point1=point1_cls,
        point2_or_vector=point2_or_vector_cls,
        diameter=diameter_cls,
    )

