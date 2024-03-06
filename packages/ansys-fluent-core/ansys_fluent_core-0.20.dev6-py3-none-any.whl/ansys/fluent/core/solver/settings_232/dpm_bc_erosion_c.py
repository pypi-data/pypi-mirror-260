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

from .method_2 import method as method_cls
from .number_of_coeff import number_of_coeff as number_of_coeff_cls
from .function_of import function_of as function_of_cls
from .coefficients_1 import coefficients as coefficients_cls
from .value_1 import value as value_cls
from .piecewise_polynomial_1 import piecewise_polynomial as piecewise_polynomial_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
class dpm_bc_erosion_c(Group):
    """
    'dpm_bc_erosion_c' child.
    """

    fluent_name = "dpm-bc-erosion-c"

    child_names = \
        ['method', 'number_of_coeff', 'function_of', 'coefficients', 'value',
         'piecewise_polynomial', 'piecewise_linear']

    _child_classes = dict(
        method=method_cls,
        number_of_coeff=number_of_coeff_cls,
        function_of=function_of_cls,
        coefficients=coefficients_cls,
        value=value_cls,
        piecewise_polynomial=piecewise_polynomial_cls,
        piecewise_linear=piecewise_linear_cls,
    )

