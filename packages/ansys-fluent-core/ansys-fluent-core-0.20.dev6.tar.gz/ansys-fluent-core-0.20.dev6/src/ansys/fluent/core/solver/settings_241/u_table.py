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
class u_table(Group):
    """
    'u_table' child.
    """

    fluent_name = "u-table"

    child_names = \
        ['row_number', 'column_number', 'row_value', 'column_value',
         'table_value']

    _child_classes = dict(
        row_number=row_number_cls,
        column_number=column_number_cls,
        row_value=row_value_cls,
        column_value=column_value_cls,
        table_value=table_value_cls,
    )

