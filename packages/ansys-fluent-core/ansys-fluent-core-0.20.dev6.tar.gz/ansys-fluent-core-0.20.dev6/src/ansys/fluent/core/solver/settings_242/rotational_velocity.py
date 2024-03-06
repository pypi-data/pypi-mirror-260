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

from .speed import speed as speed_cls
from .rotation_axis import rotation_axis as rotation_axis_cls
class rotational_velocity(Group):
    """
    'rotational_velocity' child.
    """

    fluent_name = "rotational-velocity"

    child_names = \
        ['speed', 'rotation_axis']

    _child_classes = dict(
        speed=speed_cls,
        rotation_axis=rotation_axis_cls,
    )

