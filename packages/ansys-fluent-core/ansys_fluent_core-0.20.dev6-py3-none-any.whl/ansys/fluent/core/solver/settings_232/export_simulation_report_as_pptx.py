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

from .report_name import report_name as report_name_cls
from .file_name_path import file_name_path as file_name_path_cls
class export_simulation_report_as_pptx(Command):
    """
    Export the provided simulation report as a PPT file.
    
    Parameters
    ----------
        report_name : str
            'report_name' child.
        file_name_path : str
            'file_name_path' child.
    
    """

    fluent_name = "export-simulation-report-as-pptx"

    argument_names = \
        ['report_name', 'file_name_path']

    _child_classes = dict(
        report_name=report_name_cls,
        file_name_path=file_name_path_cls,
    )

