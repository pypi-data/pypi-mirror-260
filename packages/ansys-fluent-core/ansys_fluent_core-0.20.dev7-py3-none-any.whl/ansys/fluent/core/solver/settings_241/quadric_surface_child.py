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
from .attribute import attribute as attribute_cls
from .value_1 import value as value_cls
from .display_3 import display as display_cls
class quadric_surface_child(Group):
    """
    'child_object_type' of quadric_surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'attribute', 'value']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        attribute=attribute_cls,
        value=value_cls,
        display=display_cls,
    )

