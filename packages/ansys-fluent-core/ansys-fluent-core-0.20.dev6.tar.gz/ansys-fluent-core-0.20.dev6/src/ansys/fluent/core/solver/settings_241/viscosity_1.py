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
from .piecewise_linear_1 import piecewise_linear as piecewise_linear_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .polynomial_1 import polynomial as polynomial_cls
from .expression import expression as expression_cls
from .power_law import power_law as power_law_cls
from .sutherland import sutherland as sutherland_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
from .real_gas_nist_mixture import real_gas_nist_mixture as real_gas_nist_mixture_cls
class viscosity(Group):
    """
    'viscosity' child.
    """

    fluent_name = "viscosity"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'expression', 'power_law', 'sutherland',
         'user_defined_function', 'real_gas_nist_mixture']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        piecewise_linear=piecewise_linear_cls,
        piecewise_polynomial=piecewise_polynomial_cls,
        polynomial=polynomial_cls,
        expression=expression_cls,
        power_law=power_law_cls,
        sutherland=sutherland_cls,
        user_defined_function=user_defined_function_cls,
        real_gas_nist_mixture=real_gas_nist_mixture_cls,
    )

