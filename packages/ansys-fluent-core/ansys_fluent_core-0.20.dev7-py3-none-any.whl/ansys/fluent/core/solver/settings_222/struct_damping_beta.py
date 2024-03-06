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
from .constant import constant as constant_cls
from .boussinesq import boussinesq as boussinesq_cls
from .coefficients import coefficients as coefficients_cls
from .number_of_coefficients import number_of_coefficients as number_of_coefficients_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .nasa_9_piecewise_polynomial import nasa_9_piecewise_polynomial as nasa_9_piecewise_polynomial_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .anisotropic import anisotropic as anisotropic_cls
from .orthotropic import orthotropic as orthotropic_cls
from .var_class import var_class as var_class_cls
class struct_damping_beta(Group):
    """
    'struct_damping_beta' child.
    """

    fluent_name = "struct-damping-beta"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    _child_classes = dict(
        option=option_cls,
        constant=constant_cls,
        boussinesq=boussinesq_cls,
        coefficients=coefficients_cls,
        number_of_coefficients=number_of_coefficients_cls,
        piecewise_polynomial=piecewise_polynomial_cls,
        nasa_9_piecewise_polynomial=nasa_9_piecewise_polynomial_cls,
        piecewise_linear=piecewise_linear_cls,
        anisotropic=anisotropic_cls,
        orthotropic=orthotropic_cls,
        var_class=var_class_cls,
    )

