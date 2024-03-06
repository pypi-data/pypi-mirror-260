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
from .combusting_particle_child import combusting_particle_child

class combusting_particle(NamedObject[combusting_particle_child], _CreatableNamedObjectMixin[combusting_particle_child]):
    """
    'combusting_particle' child.
    """

    fluent_name = "combusting-particle"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: combusting_particle_child = combusting_particle_child
    """
    child_object_type of combusting_particle.
    """
