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

from .write_table_1 import write_table as write_table_cls
from .read_table_1 import read_table as read_table_cls
from .print_table_1 import print_table as print_table_cls
class fast_charging_table(Group):
    """
    Set fast charging table.
    """

    fluent_name = "fast-charging-table"

    command_names = \
        ['write_table', 'read_table', 'print_table']

    _child_classes = dict(
        write_table=write_table_cls,
        read_table=read_table_cls,
        print_table=print_table_cls,
    )

