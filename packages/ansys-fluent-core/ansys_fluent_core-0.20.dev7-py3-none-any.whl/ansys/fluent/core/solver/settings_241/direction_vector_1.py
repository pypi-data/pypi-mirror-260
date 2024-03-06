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

from .x_component_1 import x_component as x_component_cls
from .y_component_1 import y_component as y_component_cls
from .z_component_1 import z_component as z_component_cls
class direction_vector(Group):
    """
    'direction_vector' child.
    """

    fluent_name = "direction-vector"

    child_names = \
        ['x_component', 'y_component', 'z_component']

    _child_classes = dict(
        x_component=x_component_cls,
        y_component=y_component_cls,
        z_component=z_component_cls,
    )

