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
from .faces import faces as faces_cls
from .list_properties_4 import list_properties as list_properties_cls
class bodies_child(Group):
    """
    'child_object_type' of bodies.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'faces']

    command_names = \
        ['list_properties']

    _child_classes = dict(
        name=name_cls,
        faces=faces_cls,
        list_properties=list_properties_cls,
    )

