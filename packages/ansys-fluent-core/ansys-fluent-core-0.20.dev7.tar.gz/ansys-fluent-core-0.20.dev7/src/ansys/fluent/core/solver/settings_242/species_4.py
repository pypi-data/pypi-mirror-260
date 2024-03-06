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

from .particle_species import particle_species as particle_species_cls
from .last_species import last_species as last_species_cls
class species(Group):
    """
    'species' child.
    """

    fluent_name = "species"

    child_names = \
        ['particle_species', 'last_species']

    _child_classes = dict(
        particle_species=particle_species_cls,
        last_species=last_species_cls,
    )

