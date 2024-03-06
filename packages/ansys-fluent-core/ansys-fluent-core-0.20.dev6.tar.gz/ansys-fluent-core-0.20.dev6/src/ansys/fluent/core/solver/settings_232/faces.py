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

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .list_face import list_face as list_face_cls
from .faces_child import faces_child

class faces(NamedObject[faces_child], _CreatableNamedObjectMixin[faces_child]):
    """
    'faces' child.
    """

    fluent_name = "faces"

    command_names = \
        ['list', 'list_properties', 'duplicate', 'list_face']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
        list_face=list_face_cls,
    )

    child_object_type: faces_child = faces_child
    """
    child_object_type of faces.
    """
