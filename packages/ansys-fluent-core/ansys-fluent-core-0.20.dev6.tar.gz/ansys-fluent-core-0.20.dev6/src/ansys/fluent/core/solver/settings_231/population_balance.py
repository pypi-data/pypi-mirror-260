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

from .moments import moments as moments_cls
from .number_density import number_density as number_density_cls
class population_balance(Group):
    """
    'population_balance' child.
    """

    fluent_name = "population-balance"

    command_names = \
        ['moments', 'number_density']

    _child_classes = dict(
        moments=moments_cls,
        number_density=number_density_cls,
    )

