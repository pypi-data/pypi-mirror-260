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

from .list_simulation_reports import list_simulation_reports as list_simulation_reports_cls
from .add_histogram_to_report import add_histogram_to_report as add_histogram_to_report_cls
from .generate_simulation_report import generate_simulation_report as generate_simulation_report_cls
from .view_simulation_report import view_simulation_report as view_simulation_report_cls
from .export_simulation_report_as_pdf import export_simulation_report_as_pdf as export_simulation_report_as_pdf_cls
from .export_simulation_report_as_html import export_simulation_report_as_html as export_simulation_report_as_html_cls
from .export_simulation_report_as_pptx import export_simulation_report_as_pptx as export_simulation_report_as_pptx_cls
from .write_simulation_report_names_to_file import write_simulation_report_names_to_file as write_simulation_report_names_to_file_cls
from .rename_simulation_report import rename_simulation_report as rename_simulation_report_cls
from .duplicate_simulation_report import duplicate_simulation_report as duplicate_simulation_report_cls
from .reset_report_to_defaults import reset_report_to_defaults as reset_report_to_defaults_cls
from .delete_simulation_report import delete_simulation_report as delete_simulation_report_cls
from .write_simulation_report_template_file import write_simulation_report_template_file as write_simulation_report_template_file_cls
from .read_simulation_report_template_file import read_simulation_report_template_file as read_simulation_report_template_file_cls
class simulation_reports(Group):
    """
    'simulation_reports' child.
    """

    fluent_name = "simulation-reports"

    command_names = \
        ['list_simulation_reports', 'add_histogram_to_report',
         'generate_simulation_report', 'view_simulation_report',
         'export_simulation_report_as_pdf',
         'export_simulation_report_as_html',
         'export_simulation_report_as_pptx',
         'write_simulation_report_names_to_file', 'rename_simulation_report',
         'duplicate_simulation_report', 'reset_report_to_defaults',
         'delete_simulation_report', 'write_simulation_report_template_file',
         'read_simulation_report_template_file']

    _child_classes = dict(
        list_simulation_reports=list_simulation_reports_cls,
        add_histogram_to_report=add_histogram_to_report_cls,
        generate_simulation_report=generate_simulation_report_cls,
        view_simulation_report=view_simulation_report_cls,
        export_simulation_report_as_pdf=export_simulation_report_as_pdf_cls,
        export_simulation_report_as_html=export_simulation_report_as_html_cls,
        export_simulation_report_as_pptx=export_simulation_report_as_pptx_cls,
        write_simulation_report_names_to_file=write_simulation_report_names_to_file_cls,
        rename_simulation_report=rename_simulation_report_cls,
        duplicate_simulation_report=duplicate_simulation_report_cls,
        reset_report_to_defaults=reset_report_to_defaults_cls,
        delete_simulation_report=delete_simulation_report_cls,
        write_simulation_report_template_file=write_simulation_report_template_file_cls,
        read_simulation_report_template_file=read_simulation_report_template_file_cls,
    )

