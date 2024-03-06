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
from .normal import normal as normal_cls
from .distance_from_origin import distance_from_origin as distance_from_origin_cls
from .display_3 import display as display_cls
class plane_slice_child(Group):
    """
    'child_object_type' of plane_slice.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'normal', 'distance_from_origin']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        normal=normal_cls,
        distance_from_origin=distance_from_origin_cls,
        display=display_cls,
    )

