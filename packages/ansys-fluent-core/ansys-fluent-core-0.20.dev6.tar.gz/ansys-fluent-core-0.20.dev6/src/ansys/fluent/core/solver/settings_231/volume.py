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

from .volume_child import volume_child

class volume(NamedObject[volume_child], _CreatableNamedObjectMixin[volume_child]):
    """
    'volume' child.
    """

    fluent_name = "volume"

    child_object_type: volume_child = volume_child
    """
    child_object_type of volume.
    """
