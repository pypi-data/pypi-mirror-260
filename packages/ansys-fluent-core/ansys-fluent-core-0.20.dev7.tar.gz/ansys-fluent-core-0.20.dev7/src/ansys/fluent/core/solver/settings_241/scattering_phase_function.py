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
from .delta_eddington import delta_eddington as delta_eddington_cls
from .user_defined_function import user_defined_function as user_defined_function_cls
class scattering_phase_function(Group):
    """
    'scattering_phase_function' child.
    """

    fluent_name = "scattering-phase-function"

    child_names = \
        ['option', 'value', 'delta_eddington', 'user_defined_function']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        delta_eddington=delta_eddington_cls,
        user_defined_function=user_defined_function_cls,
    )

