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

from .name import name as name_cls
from .x_component import x_component as x_component_cls
from .y_component import y_component as y_component_cls
from .z_component import z_component as z_component_cls
class custom_vectors_child(Group):
    """
    'child_object_type' of custom_vectors.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'x_component', 'y_component', 'z_component']

    _child_classes = dict(
        name=name_cls,
        x_component=x_component_cls,
        y_component=y_component_cls,
        z_component=z_component_cls,
    )

