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

from .report_definitions_1 import report_definitions as report_definitions_cls
from .list_5 import list as list_cls
from .print_all_to_console import print_all_to_console as print_all_to_console_cls
from .write_all_to_file import write_all_to_file as write_all_to_file_cls
class output_parameters(Group):
    """
    Enter the output-parameters menu.
    """

    fluent_name = "output-parameters"

    child_names = \
        ['report_definitions']

    command_names = \
        ['list', 'print_all_to_console', 'write_all_to_file']

    _child_classes = dict(
        report_definitions=report_definitions_cls,
        list=list_cls,
        print_all_to_console=print_all_to_console_cls,
        write_all_to_file=write_all_to_file_cls,
    )

