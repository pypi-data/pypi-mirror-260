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
from .type_4 import type as type_cls
from .phase_32 import phase as phase_cls
from .boundaries import boundaries as boundaries_cls
from .location_2 import location as location_cls
class fluid_child(Group):
    """
    'child_object_type' of fluid.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'type', 'phase', 'boundaries', 'location']

    _child_classes = dict(
        name=name_cls,
        type=type_cls,
        phase=phase_cls,
        boundaries=boundaries_cls,
        location=location_cls,
    )

