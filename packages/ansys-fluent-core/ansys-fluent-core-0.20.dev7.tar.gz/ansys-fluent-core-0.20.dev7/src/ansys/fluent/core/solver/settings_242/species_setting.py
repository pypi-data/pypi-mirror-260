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

from .user_specified_species import user_specified_species as user_specified_species_cls
from .species_12 import species as species_cls
class species_setting(Group):
    """
    Enter the species settings menu.
    """

    fluent_name = "species-setting"

    child_names = \
        ['user_specified_species', 'species']

    _child_classes = dict(
        user_specified_species=user_specified_species_cls,
        species=species_cls,
    )

