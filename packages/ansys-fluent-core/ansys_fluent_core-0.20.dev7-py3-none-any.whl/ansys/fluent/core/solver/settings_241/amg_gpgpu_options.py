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
from .amg_gpgpu_options_child import amg_gpgpu_options_child

class amg_gpgpu_options(NamedObject[amg_gpgpu_options_child], _NonCreatableNamedObjectMixin[amg_gpgpu_options_child]):
    """
    Enter AMG GPGPU options menu.
    """

    fluent_name = "amg-gpgpu-options"

    command_names = \
        ['delete', 'list', 'list_properties', 'make_a_copy']

    _child_classes = dict(
        delete=delete_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
    )

    child_object_type: amg_gpgpu_options_child = amg_gpgpu_options_child
    """
    child_object_type of amg_gpgpu_options.
    """
