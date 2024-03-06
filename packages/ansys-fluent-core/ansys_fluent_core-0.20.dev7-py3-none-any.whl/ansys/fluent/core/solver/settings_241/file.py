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

from .single_precision_coordinates import single_precision_coordinates as single_precision_coordinates_cls
from .binary_legacy_files import binary_legacy_files as binary_legacy_files_cls
from .cff_files import cff_files as cff_files_cls
from .convert_hanging_nodes_during_read import convert_hanging_nodes_during_read as convert_hanging_nodes_during_read_cls
from .async_optimize import async_optimize as async_optimize_cls
from .write_pdat import write_pdat as write_pdat_cls
from .auto_save import auto_save as auto_save_cls
from .export import export as export_cls
from .import_ import import_ as import__cls
from .parametric_project import parametric_project as parametric_project_cls
from .cffio_options import cffio_options as cffio_options_cls
from .batch_options import batch_options as batch_options_cls
from .define_macro import define_macro as define_macro_cls
from .execute_macro import execute_macro as execute_macro_cls
from .read_macros import read_macros as read_macros_cls
from .read_1 import read as read_cls
from .read_case import read_case as read_case_cls
from .read_case_data import read_case_data as read_case_data_cls
from .read_case_setting import read_case_setting as read_case_setting_cls
from .read_data import read_data as read_data_cls
from .read_mesh import read_mesh as read_mesh_cls
from .read_surface_mesh import read_surface_mesh as read_surface_mesh_cls
from .read_journal import read_journal as read_journal_cls
from .start_journal import start_journal as start_journal_cls
from .stop_journal import stop_journal as stop_journal_cls
from .replace_mesh import replace_mesh as replace_mesh_cls
from .write import write as write_cls
from .write_case import write_case as write_case_cls
from .write_data import write_data as write_data_cls
from .write_case_data import write_case_data as write_case_data_cls
from .read_settings import read_settings as read_settings_cls
from .read_field_functions import read_field_functions as read_field_functions_cls
from .read_injections import read_injections as read_injections_cls
from .read_profile import read_profile as read_profile_cls
from .read_pdf import read_pdf as read_pdf_cls
from .read_isat_table import read_isat_table as read_isat_table_cls
from .show_configuration import show_configuration as show_configuration_cls
from .stop_macro import stop_macro as stop_macro_cls
from .start_transcript import start_transcript as start_transcript_cls
from .stop_transcript import stop_transcript as stop_transcript_cls
from .data_file_options import data_file_options as data_file_options_cls
class file(Group):
    """
    'file' child.
    """

    fluent_name = "file"

    child_names = \
        ['single_precision_coordinates', 'binary_legacy_files', 'cff_files',
         'convert_hanging_nodes_during_read', 'async_optimize', 'write_pdat',
         'auto_save', 'export', 'import_', 'parametric_project',
         'cffio_options', 'batch_options']

    command_names = \
        ['define_macro', 'execute_macro', 'read_macros', 'read', 'read_case',
         'read_case_data', 'read_case_setting', 'read_data', 'read_mesh',
         'read_surface_mesh', 'read_journal', 'start_journal', 'stop_journal',
         'replace_mesh', 'write', 'write_case', 'write_data',
         'write_case_data', 'read_settings', 'read_field_functions',
         'read_injections', 'read_profile', 'read_pdf', 'read_isat_table',
         'show_configuration', 'stop_macro', 'start_transcript',
         'stop_transcript', 'data_file_options']

    _child_classes = dict(
        single_precision_coordinates=single_precision_coordinates_cls,
        binary_legacy_files=binary_legacy_files_cls,
        cff_files=cff_files_cls,
        convert_hanging_nodes_during_read=convert_hanging_nodes_during_read_cls,
        async_optimize=async_optimize_cls,
        write_pdat=write_pdat_cls,
        auto_save=auto_save_cls,
        export=export_cls,
        import_=import__cls,
        parametric_project=parametric_project_cls,
        cffio_options=cffio_options_cls,
        batch_options=batch_options_cls,
        define_macro=define_macro_cls,
        execute_macro=execute_macro_cls,
        read_macros=read_macros_cls,
        read=read_cls,
        read_case=read_case_cls,
        read_case_data=read_case_data_cls,
        read_case_setting=read_case_setting_cls,
        read_data=read_data_cls,
        read_mesh=read_mesh_cls,
        read_surface_mesh=read_surface_mesh_cls,
        read_journal=read_journal_cls,
        start_journal=start_journal_cls,
        stop_journal=stop_journal_cls,
        replace_mesh=replace_mesh_cls,
        write=write_cls,
        write_case=write_case_cls,
        write_data=write_data_cls,
        write_case_data=write_case_data_cls,
        read_settings=read_settings_cls,
        read_field_functions=read_field_functions_cls,
        read_injections=read_injections_cls,
        read_profile=read_profile_cls,
        read_pdf=read_pdf_cls,
        read_isat_table=read_isat_table_cls,
        show_configuration=show_configuration_cls,
        stop_macro=stop_macro_cls,
        start_transcript=start_transcript_cls,
        stop_transcript=stop_transcript_cls,
        data_file_options=data_file_options_cls,
    )

