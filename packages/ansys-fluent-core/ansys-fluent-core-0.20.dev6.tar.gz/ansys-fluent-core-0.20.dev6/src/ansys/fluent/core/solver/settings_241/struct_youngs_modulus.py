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
from .value_3 import value as value_cls
from .orthotropic_structure_ym import orthotropic_structure_ym as orthotropic_structure_ym_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class struct_youngs_modulus(Group):
    """
    'struct_youngs_modulus' child.
    """

    fluent_name = "struct-youngs-modulus"

    child_names = \
        ['option', 'value', 'orthotropic_structure_ym',
         'user_defined_function']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        orthotropic_structure_ym=orthotropic_structure_ym_cls,
        user_defined_function=user_defined_function_cls,
    )

