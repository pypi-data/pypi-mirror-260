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

from .enable_1 import enable as enable_cls
from .disable import disable as disable_cls
from .print import print as print_cls
from .clear import clear as clear_cls
class profile(Group):
    """
    Enter the adaption profile menu.
    """

    fluent_name = "profile"

    command_names = \
        ['enable', 'disable', 'print', 'clear']

    _child_classes = dict(
        enable=enable_cls,
        disable=disable_cls,
        print=print_cls,
        clear=clear_cls,
    )

