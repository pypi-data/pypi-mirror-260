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

from .number_density import number_density as number_density_cls
from .moments import moments as moments_cls
class population_balance(Group):
    """
    'population_balance' child.
    """

    fluent_name = "population-balance"

    child_names = \
        ['number_density']

    command_names = \
        ['moments']

    _child_classes = dict(
        number_density=number_density_cls,
        moments=moments_cls,
    )

