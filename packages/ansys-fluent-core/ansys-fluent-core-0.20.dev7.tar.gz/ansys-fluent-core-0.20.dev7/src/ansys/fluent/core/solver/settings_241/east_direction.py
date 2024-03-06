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

from .east_x import east_x as east_x_cls
from .east_y import east_y as east_y_cls
from .east_z import east_z as east_z_cls
class east_direction(Group):
    """
    'east_direction' child.
    """

    fluent_name = "east-direction"

    child_names = \
        ['east_x', 'east_y', 'east_z']

    _child_classes = dict(
        east_x=east_x_cls,
        east_y=east_y_cls,
        east_z=east_z_cls,
    )

