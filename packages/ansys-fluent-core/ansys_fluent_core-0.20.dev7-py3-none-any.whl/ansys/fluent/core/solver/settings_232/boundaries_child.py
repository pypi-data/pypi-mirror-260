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

from .type_4 import type as type_cls
from .locations import locations as locations_cls
class boundaries_child(Group):
    """
    'child_object_type' of boundaries.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['type', 'locations']

    _child_classes = dict(
        type=type_cls,
        locations=locations_cls,
    )

