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

from .option_10 import option as option_cls
from .species_diffusivity import species_diffusivity as species_diffusivity_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class thermal_diffusivity(Group):
    """
    'thermal_diffusivity' child.
    """

    fluent_name = "thermal-diffusivity"

    child_names = \
        ['option', 'species_diffusivity', 'user_defined_function']

    _child_classes = dict(
        option=option_cls,
        species_diffusivity=species_diffusivity_cls,
        user_defined_function=user_defined_function_cls,
    )

