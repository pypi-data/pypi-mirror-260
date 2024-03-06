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

from .print_3 import print as print_cls
from .write_2 import write as write_cls
class histogram(Group):
    """
    'histogram' child.
    """

    fluent_name = "histogram"

    command_names = \
        ['print', 'write']

    _child_classes = dict(
        print=print_cls,
        write=write_cls,
    )

