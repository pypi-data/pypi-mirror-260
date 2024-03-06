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
from .value_1 import value as value_cls
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .polynomial import polynomial as polynomial_cls
from .expression import expression as expression_cls
from .power_law import power_law as power_law_cls
from .blottner_curve_fit import blottner_curve_fit as blottner_curve_fit_cls
from .gupta_curve_fit_viscosity import gupta_curve_fit_viscosity as gupta_curve_fit_viscosity_cls
from .sutherland import sutherland as sutherland_cls
from .cross import cross as cross_cls
from .herschel_bulkley import herschel_bulkley as herschel_bulkley_cls
from .carreau import carreau as carreau_cls
from .non_newtonian_power_law import non_newtonian_power_law as non_newtonian_power_law_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
from .rgp_table import rgp_table as rgp_table_cls
from .real_gas_nist import real_gas_nist as real_gas_nist_cls
class viscosity(Group):
    """
    'viscosity' child.
    """

    fluent_name = "viscosity"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'expression', 'power_law', 'blottner_curve_fit',
         'gupta_curve_fit_viscosity', 'sutherland', 'cross',
         'herschel_bulkley', 'carreau', 'non_newtonian_power_law',
         'user_defined_function', 'rgp_table', 'real_gas_nist']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        piecewise_linear=piecewise_linear_cls,
        piecewise_polynomial=piecewise_polynomial_cls,
        polynomial=polynomial_cls,
        expression=expression_cls,
        power_law=power_law_cls,
        blottner_curve_fit=blottner_curve_fit_cls,
        gupta_curve_fit_viscosity=gupta_curve_fit_viscosity_cls,
        sutherland=sutherland_cls,
        cross=cross_cls,
        herschel_bulkley=herschel_bulkley_cls,
        carreau=carreau_cls,
        non_newtonian_power_law=non_newtonian_power_law_cls,
        user_defined_function=user_defined_function_cls,
        rgp_table=rgp_table_cls,
        real_gas_nist=real_gas_nist_cls,
    )

