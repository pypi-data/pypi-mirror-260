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
from .user_defined_function import user_defined_function as user_defined_function_cls
class premix_unburnt_temp(Group):
    """
    'premix_unburnt_temp' child.
    """

    fluent_name = "premix-unburnt-temp"

    child_names = \
        ['option', 'user_defined_function']

    _child_classes = dict(
        option=option_cls,
        user_defined_function=user_defined_function_cls,
    )

