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
from .type_5 import type as type_cls
from .location_2 import location as location_cls
from .phase_43 import phase as phase_cls
class network_end_child(Group):
    """
    'child_object_type' of network_end.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'type', 'location', 'phase']

    _child_classes = dict(
        name=name_cls,
        type=type_cls,
        location=location_cls,
        phase=phase_cls,
    )

