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

from .pre_exponential_factor import pre_exponential_factor as pre_exponential_factor_cls
from .activation_energy import activation_energy as activation_energy_cls
from .weighting_factor import weighting_factor as weighting_factor_cls
class second_rate(Group):
    """
    'second_rate' child.
    """

    fluent_name = "second-rate"

    child_names = \
        ['pre_exponential_factor', 'activation_energy', 'weighting_factor']

    _child_classes = dict(
        pre_exponential_factor=pre_exponential_factor_cls,
        activation_energy=activation_energy_cls,
        weighting_factor=weighting_factor_cls,
    )

