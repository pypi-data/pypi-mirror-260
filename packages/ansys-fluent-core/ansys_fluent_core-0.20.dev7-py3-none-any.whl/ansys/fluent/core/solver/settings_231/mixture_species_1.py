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

from .droplet_particle_child import droplet_particle_child

class mixture_species(NamedObject[droplet_particle_child], _NonCreatableNamedObjectMixin[droplet_particle_child]):
    """
    'mixture_species' child.
    """

    fluent_name = "mixture-species"

    child_object_type: droplet_particle_child = droplet_particle_child
    """
    child_object_type of mixture_species.
    """
