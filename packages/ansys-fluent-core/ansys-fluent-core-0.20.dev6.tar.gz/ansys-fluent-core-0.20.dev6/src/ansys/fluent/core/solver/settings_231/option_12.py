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
from .yplus_1 import yplus as yplus_cls
from .ystar import ystar as ystar_cls
class option(Group):
    """
    'option' child.
    """

    fluent_name = "option"

    child_names = \
        ['option', 'yplus', 'ystar']

    _child_classes = dict(
        option=option_cls,
        yplus=yplus_cls,
        ystar=ystar_cls,
    )

