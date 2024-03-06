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

from .linear_velocity import linear_velocity as linear_velocity_cls
from .rotational_velocity import rotational_velocity as rotational_velocity_cls
class constant_velocity(Group):
    """
    'constant_velocity' child.
    """

    fluent_name = "constant-velocity"

    child_names = \
        ['linear_velocity', 'rotational_velocity']

    _child_classes = dict(
        linear_velocity=linear_velocity_cls,
        rotational_velocity=rotational_velocity_cls,
    )

