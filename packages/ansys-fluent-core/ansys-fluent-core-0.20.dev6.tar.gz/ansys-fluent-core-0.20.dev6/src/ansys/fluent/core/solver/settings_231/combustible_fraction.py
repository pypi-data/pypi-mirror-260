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
class combustible_fraction(Group):
    """
    'combustible_fraction' child.
    """

    fluent_name = "combustible-fraction"

    child_names = \
        ['option', 'value']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
    )

