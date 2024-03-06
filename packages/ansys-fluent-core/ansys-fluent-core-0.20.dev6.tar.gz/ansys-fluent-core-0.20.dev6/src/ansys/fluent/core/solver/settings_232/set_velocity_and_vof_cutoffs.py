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
from .set_velocity_and_vof_cutoffs_child import set_velocity_and_vof_cutoffs_child

class set_velocity_and_vof_cutoffs(NamedObject[set_velocity_and_vof_cutoffs_child], _NonCreatableNamedObjectMixin[set_velocity_and_vof_cutoffs_child]):
    """
    'set_velocity_and_vof_cutoffs' child.
    """

    fluent_name = "set-velocity-and-vof-cutoffs"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: set_velocity_and_vof_cutoffs_child = set_velocity_and_vof_cutoffs_child
    """
    child_object_type of set_velocity_and_vof_cutoffs.
    """
