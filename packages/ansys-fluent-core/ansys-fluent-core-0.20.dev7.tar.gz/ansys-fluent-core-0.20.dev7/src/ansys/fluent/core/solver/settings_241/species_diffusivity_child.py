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

from .option_7 import option as option_cls
from .value_3 import value as value_cls
from .polynomial_1 import polynomial as polynomial_cls
class species_diffusivity_child(Group):
    """
    'child_object_type' of species_diffusivity.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['option', 'value', 'polynomial']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        polynomial=polynomial_cls,
    )

