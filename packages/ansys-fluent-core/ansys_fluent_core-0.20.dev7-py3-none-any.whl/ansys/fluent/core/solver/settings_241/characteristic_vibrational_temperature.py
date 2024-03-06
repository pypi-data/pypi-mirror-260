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
from .vibrational_modes import vibrational_modes as vibrational_modes_cls
from .value_3 import value as value_cls
class characteristic_vibrational_temperature(Group):
    """
    'characteristic_vibrational_temperature' child.
    """

    fluent_name = "characteristic-vibrational-temperature"

    child_names = \
        ['option', 'vibrational_modes', 'value']

    _child_classes = dict(
        option=option_cls,
        vibrational_modes=vibrational_modes_cls,
        value=value_cls,
    )

