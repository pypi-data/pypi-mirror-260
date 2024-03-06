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
from .output_dir import output_dir as output_dir_cls
class export_simulation_report_as_html(Command):
    """
    Export the provided simulation report as HTML.
    
    Parameters
    ----------
        report_name : str
            'report_name' child.
        output_dir : str
            'output_dir' child.
    
    """

    fluent_name = "export-simulation-report-as-html"

    argument_names = \
        ['report_name', 'output_dir']

    _child_classes = dict(
        report_name=report_name_cls,
        output_dir=output_dir_cls,
    )

