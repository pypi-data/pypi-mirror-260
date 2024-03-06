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
from .value import value as value_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .polynomial import polynomial as polynomial_cls
from .expression import expression as expression_cls
from .biaxial import biaxial as biaxial_cls
from .cyl_orthotropic_1 import cyl_orthotropic as cyl_orthotropic_cls
from .orthotropic_1 import orthotropic as orthotropic_cls
from .principal_axes_values import principal_axes_values as principal_axes_values_cls
from .anisotropic_1 import anisotropic as anisotropic_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class thermal_conductivity(Group):
    """
    'thermal_conductivity' child.
    """

    fluent_name = "thermal-conductivity"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'expression', 'biaxial', 'cyl_orthotropic',
         'orthotropic', 'principal_axes_values', 'anisotropic',
         'user_defined_function']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        piecewise_linear=piecewise_linear_cls,
        piecewise_polynomial=piecewise_polynomial_cls,
        polynomial=polynomial_cls,
        expression=expression_cls,
        biaxial=biaxial_cls,
        cyl_orthotropic=cyl_orthotropic_cls,
        orthotropic=orthotropic_cls,
        principal_axes_values=principal_axes_values_cls,
        anisotropic=anisotropic_cls,
        user_defined_function=user_defined_function_cls,
    )

