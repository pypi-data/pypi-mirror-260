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
from .real_gas_nist import real_gas_nist as real_gas_nist_cls
from .value import value as value_cls
from .compressible_liquid import compressible_liquid as compressible_liquid_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .polynomial import polynomial as polynomial_cls
from .expression import expression as expression_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
from .rgp_table import rgp_table as rgp_table_cls
class density(Group):
    """
    'density' child.
    """

    fluent_name = "density"

    child_names = \
        ['option', 'real_gas_nist', 'value', 'compressible_liquid',
         'piecewise_linear', 'piecewise_polynomial', 'polynomial',
         'expression', 'user_defined_function', 'rgp_table']

    _child_classes = dict(
        option=option_cls,
        real_gas_nist=real_gas_nist_cls,
        value=value_cls,
        compressible_liquid=compressible_liquid_cls,
        piecewise_linear=piecewise_linear_cls,
        piecewise_polynomial=piecewise_polynomial_cls,
        polynomial=polynomial_cls,
        expression=expression_cls,
        user_defined_function=user_defined_function_cls,
        rgp_table=rgp_table_cls,
    )

