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

from .report_files_child import report_files_child

class report_files(NamedObject[report_files_child], _CreatableNamedObjectMixin[report_files_child]):
    """
    'report_files' child.
    """

    fluent_name = "report-files"

    child_object_type: report_files_child = report_files_child
    """
    child_object_type of report_files.
    """
