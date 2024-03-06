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

from .amg_gpgpu_options_child import amg_gpgpu_options_child

class amg_gpgpu_options(NamedObject[amg_gpgpu_options_child], _CreatableNamedObjectMixin[amg_gpgpu_options_child]):
    """
    'amg_gpgpu_options' child.
    """

    fluent_name = "amg-gpgpu-options"

    child_object_type: amg_gpgpu_options_child = amg_gpgpu_options_child
    """
    child_object_type of amg_gpgpu_options.
    """
