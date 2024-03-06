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

from .north_x import north_x as north_x_cls
from .north_y import north_y as north_y_cls
from .north_z import north_z as north_z_cls
class north_direction(Group):
    """
    'north_direction' child.
    """

    fluent_name = "north-direction"

    child_names = \
        ['north_x', 'north_y', 'north_z']

    _child_classes = dict(
        north_x=north_x_cls,
        north_y=north_y_cls,
        north_z=north_z_cls,
    )

