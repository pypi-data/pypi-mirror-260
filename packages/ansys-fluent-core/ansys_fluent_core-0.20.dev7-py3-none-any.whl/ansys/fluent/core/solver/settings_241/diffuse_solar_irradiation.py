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
from .piecewise_linear import piecewise_linear as piecewise_linear_cls
from .polynomial import polynomial as polynomial_cls
from .user_defined_4 import user_defined as user_defined_cls
class diffuse_solar_irradiation(Group):
    """
    'diffuse_solar_irradiation' child.
    """

    fluent_name = "diffuse-solar-irradiation"

    child_names = \
        ['option', 'constant', 'piecewise_linear', 'polynomial',
         'user_defined']

    _child_classes = dict(
        option=option_cls,
        constant=constant_cls,
        piecewise_linear=piecewise_linear_cls,
        polynomial=polynomial_cls,
        user_defined=user_defined_cls,
    )

