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

from .first_rate import first_rate as first_rate_cls
from .second_rate import second_rate as second_rate_cls
class two_competing_rates(Group):
    """
    'two_competing_rates' child.
    """

    fluent_name = "two-competing-rates"

    child_names = \
        ['first_rate', 'second_rate']

    _child_classes = dict(
        first_rate=first_rate_cls,
        second_rate=second_rate_cls,
    )

