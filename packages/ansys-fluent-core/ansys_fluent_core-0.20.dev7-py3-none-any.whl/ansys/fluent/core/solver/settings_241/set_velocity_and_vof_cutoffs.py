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

from .delete_1 import delete as delete_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .set_velocity_and_vof_cutoffs_child import set_velocity_and_vof_cutoffs_child

class set_velocity_and_vof_cutoffs(NamedObject[set_velocity_and_vof_cutoffs_child], _NonCreatableNamedObjectMixin[set_velocity_and_vof_cutoffs_child]):
    """
    Set velocity and vof cutoff.
    """

    fluent_name = "set-velocity-and-vof-cutoffs"

    command_names = \
        ['delete', 'list', 'list_properties', 'make_a_copy']

    _child_classes = dict(
        delete=delete_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
    )

    child_object_type: set_velocity_and_vof_cutoffs_child = set_velocity_and_vof_cutoffs_child
    """
    child_object_type of set_velocity_and_vof_cutoffs.
    """
