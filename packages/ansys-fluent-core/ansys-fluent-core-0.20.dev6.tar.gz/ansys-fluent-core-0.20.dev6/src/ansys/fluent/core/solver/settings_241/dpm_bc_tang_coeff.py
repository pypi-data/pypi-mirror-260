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

from .option import option as option_cls
from .function_of import function_of as function_of_cls
from .value_4 import value as value_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .piecewise_linear_1 import piecewise_linear as piecewise_linear_cls
from .polynomial_1 import polynomial as polynomial_cls
class dpm_bc_tang_coeff(Group):
    """
    Tangent.
    """

    fluent_name = "dpm-bc-tang-coeff"

    child_names = \
        ['option', 'function_of', 'value', 'piecewise_polynomial',
         'piecewise_linear', 'polynomial']

    _child_classes = dict(
        option=option_cls,
        function_of=function_of_cls,
        value=value_cls,
        piecewise_polynomial=piecewise_polynomial_cls,
        piecewise_linear=piecewise_linear_cls,
        polynomial=polynomial_cls,
    )

