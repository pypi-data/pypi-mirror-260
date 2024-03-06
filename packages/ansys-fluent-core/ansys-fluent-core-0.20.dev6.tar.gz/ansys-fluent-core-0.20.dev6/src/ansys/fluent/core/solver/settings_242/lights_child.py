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

from .on import on as on_cls
from .rgb import rgb as rgb_cls
from .direction_3 import direction as direction_cls
from .set_direction_from_view_vector import set_direction_from_view_vector as set_direction_from_view_vector_cls
class lights_child(Group):
    """
    'child_object_type' of lights.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['on', 'rgb', 'direction']

    command_names = \
        ['set_direction_from_view_vector']

    _child_classes = dict(
        on=on_cls,
        rgb=rgb_cls,
        direction=direction_cls,
        set_direction_from_view_vector=set_direction_from_view_vector_cls,
    )

