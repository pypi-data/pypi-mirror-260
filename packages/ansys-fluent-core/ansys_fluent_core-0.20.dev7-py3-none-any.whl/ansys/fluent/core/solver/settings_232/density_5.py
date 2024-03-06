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
from .compressible_liquid import compressible_liquid as compressible_liquid_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
from .value_1 import value as value_cls
class density(Group):
    """
    'density' child.
    """

    fluent_name = "density"

    child_names = \
        ['option', 'compressible_liquid', 'user_defined_function', 'value']

    _child_classes = dict(
        option=option_cls,
        compressible_liquid=compressible_liquid_cls,
        user_defined_function=user_defined_function_cls,
        value=value_cls,
    )

