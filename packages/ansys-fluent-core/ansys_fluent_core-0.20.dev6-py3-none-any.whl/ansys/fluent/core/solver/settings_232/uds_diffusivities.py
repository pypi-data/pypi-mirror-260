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
from .uds_diffusivities_child import uds_diffusivities_child

class uds_diffusivities(NamedObject[uds_diffusivities_child], _NonCreatableNamedObjectMixin[uds_diffusivities_child]):
    """
    'uds_diffusivities' child.
    """

    fluent_name = "uds-diffusivities"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: uds_diffusivities_child = uds_diffusivities_child
    """
    child_object_type of uds_diffusivities.
    """
