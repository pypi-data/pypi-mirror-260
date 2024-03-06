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
from .general_1 import general as general_cls
from .geometry_1 import geometry as geometry_cls
from .trimming import trimming as trimming_cls
class rotor_child(Group):
    """
    'child_object_type' of rotor.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'general', 'geometry', 'trimming']

    _child_classes = dict(
        name=name_cls,
        general=general_cls,
        geometry=geometry_cls,
        trimming=trimming_cls,
    )

