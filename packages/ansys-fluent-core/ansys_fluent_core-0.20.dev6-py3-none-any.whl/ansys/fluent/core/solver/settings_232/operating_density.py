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

from .enable_3 import enable as enable_cls
from .method import method as method_cls
from .value import value as value_cls
from .print_1 import print as print_cls
class operating_density(Group):
    """
    Enable/disable use of a specified operating density.
    """

    fluent_name = "operating-density"

    child_names = \
        ['enable', 'method', 'value']

    command_names = \
        ['print']

    _child_classes = dict(
        enable=enable_cls,
        method=method_cls,
        value=value_cls,
        print=print_cls,
    )

