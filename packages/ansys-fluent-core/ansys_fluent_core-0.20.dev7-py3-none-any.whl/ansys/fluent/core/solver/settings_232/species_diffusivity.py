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
from .species_diffusivity_child import species_diffusivity_child

class species_diffusivity(NamedObject[species_diffusivity_child], _NonCreatableNamedObjectMixin[species_diffusivity_child]):
    """
    'species_diffusivity' child.
    """

    fluent_name = "species-diffusivity"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: species_diffusivity_child = species_diffusivity_child
    """
    child_object_type of species_diffusivity.
    """
