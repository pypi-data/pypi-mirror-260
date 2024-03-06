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

from .option import option as option_cls
from .distance import distance as distance_cls
from .x_coordinates import x_coordinates as x_coordinates_cls
from .y_coordinates import y_coordinates as y_coordinates_cls
from .z_coordinates import z_coordinates as z_coordinates_cls
class x_axis_quantity(Group):
    """
    'x_axis_quantity' child.
    """

    fluent_name = "x-axis-quantity"

    child_names = \
        ['option', 'distance', 'x_coordinates', 'y_coordinates',
         'z_coordinates']

    _child_classes = dict(
        option=option_cls,
        distance=distance_cls,
        x_coordinates=x_coordinates_cls,
        y_coordinates=y_coordinates_cls,
        z_coordinates=z_coordinates_cls,
    )

