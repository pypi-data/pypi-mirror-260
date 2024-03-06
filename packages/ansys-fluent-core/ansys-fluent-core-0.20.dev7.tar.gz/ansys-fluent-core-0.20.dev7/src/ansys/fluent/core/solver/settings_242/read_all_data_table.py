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

from .enabled_14 import enabled as enabled_cls
from .file_name_1_5 import file_name_1 as file_name_1_cls
class read_all_data_table(Command):
    """
    Command to read all ECM data tables.
    
    Parameters
    ----------
        enabled : bool
            Read all ECM data tables.
        file_name_1 : str
            File name in reading ECM tables.
    
    """

    fluent_name = "read-all-data-table"

    argument_names = \
        ['enabled', 'file_name']

    _child_classes = dict(
        enabled=enabled_cls,
        file_name=file_name_1_cls,
    )

