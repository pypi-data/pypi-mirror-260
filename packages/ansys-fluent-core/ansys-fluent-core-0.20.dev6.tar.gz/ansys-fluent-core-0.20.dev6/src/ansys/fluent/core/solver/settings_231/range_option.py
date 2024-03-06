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

from .option_3 import option as option_cls
from .auto_range_on import auto_range_on as auto_range_on_cls
from .auto_range_off import auto_range_off as auto_range_off_cls
class range_option(Group):
    """
    'range_option' child.
    """

    fluent_name = "range-option"

    child_names = \
        ['option', 'auto_range_on', 'auto_range_off']

    _child_classes = dict(
        option=option_cls,
        auto_range_on=auto_range_on_cls,
        auto_range_off=auto_range_off_cls,
    )

