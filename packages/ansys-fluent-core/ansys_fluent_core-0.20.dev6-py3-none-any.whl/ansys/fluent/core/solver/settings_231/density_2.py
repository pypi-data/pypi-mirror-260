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
from .real_gas_nist_mixture import real_gas_nist_mixture as real_gas_nist_mixture_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class density(Group):
    """
    'density' child.
    """

    fluent_name = "density"

    child_names = \
        ['option', 'real_gas_nist_mixture', 'user_defined_function']

    _child_classes = dict(
        option=option_cls,
        real_gas_nist_mixture=real_gas_nist_mixture_cls,
        user_defined_function=user_defined_function_cls,
    )

