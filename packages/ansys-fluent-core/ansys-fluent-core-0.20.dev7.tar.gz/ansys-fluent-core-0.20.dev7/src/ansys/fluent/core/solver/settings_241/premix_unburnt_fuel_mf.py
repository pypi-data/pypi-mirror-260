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
from .user_defined_function import user_defined_function as user_defined_function_cls
class premix_unburnt_fuel_mf(Group):
    """
    'premix_unburnt_fuel_mf' child.
    """

    fluent_name = "premix-unburnt-fuel-mf"

    child_names = \
        ['option', 'value', 'user_defined_function']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        user_defined_function=user_defined_function_cls,
    )

