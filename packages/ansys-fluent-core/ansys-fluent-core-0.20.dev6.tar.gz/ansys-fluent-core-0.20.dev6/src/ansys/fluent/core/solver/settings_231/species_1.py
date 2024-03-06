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

from .species_child import species_child

class species(NamedObject[species_child], _NonCreatableNamedObjectMixin[species_child]):
    """
    'species' child.
    """

    fluent_name = "species"

    child_object_type: species_child = species_child
    """
    child_object_type of species.
    """
