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

from .row_number import row_number as row_number_cls
from .column_number import column_number as column_number_cls
from .row_value import row_value as row_value_cls
from .column_value import column_value as column_value_cls
from .table_value import table_value as table_value_cls
from .write_table import write_table as write_table_cls
from .read_table import read_table as read_table_cls
from .print_table import print_table as print_table_cls
class table_r2_c(Group):
    """
    Charging r2 table data in the ECM model.
    """

    fluent_name = "table-r2-c"

    child_names = \
        ['row_number', 'column_number', 'row_value', 'column_value',
         'table_value']

    command_names = \
        ['write_table', 'read_table', 'print_table']

    _child_classes = dict(
        row_number=row_number_cls,
        column_number=column_number_cls,
        row_value=row_value_cls,
        column_value=column_value_cls,
        table_value=table_value_cls,
        write_table=write_table_cls,
        read_table=read_table_cls,
        print_table=print_table_cls,
    )

