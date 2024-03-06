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
from .zone_name_1 import zone_name as zone_name_cls
from .display_3 import display as display_cls
class zone_surface_child(Group):
    """
    'child_object_type' of zone_surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'zone_name']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        zone_name=zone_name_cls,
        display=display_cls,
    )

