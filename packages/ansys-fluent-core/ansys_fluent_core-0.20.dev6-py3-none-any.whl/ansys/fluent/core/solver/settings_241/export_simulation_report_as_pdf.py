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
from .file_name_1 import file_name as file_name_cls
class export_simulation_report_as_pdf(Command):
    """
    Export the provided simulation report as a PDF file.
    
    Parameters
    ----------
        report_name : str
            'report_name' child.
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "export-simulation-report-as-pdf"

    argument_names = \
        ['report_name', 'file_name']

    _child_classes = dict(
        report_name=report_name_cls,
        file_name=file_name_cls,
    )

