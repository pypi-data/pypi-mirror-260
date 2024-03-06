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

from .rom_type import rom_type as rom_type_cls
from .transient_setup import transient_setup as transient_setup_cls
from .file_saving_frequency import file_saving_frequency as file_saving_frequency_cls
from .joule_heat_parameter import joule_heat_parameter as joule_heat_parameter_cls
from .add_rom_parameter import add_rom_parameter as add_rom_parameter_cls
from .rom_data_creator import rom_data_creator as rom_data_creator_cls
from .create_journal_file import create_journal_file as create_journal_file_cls
from .list_rom_parameter import list_rom_parameter as list_rom_parameter_cls
from .delete_rom_parameter import delete_rom_parameter as delete_rom_parameter_cls
class rom_data_creator_tool(Group):
    """
    Set rom tool kit.
    """

    fluent_name = "rom-data-creator-tool"

    child_names = \
        ['rom_type', 'transient_setup', 'file_saving_frequency',
         'joule_heat_parameter']

    command_names = \
        ['add_rom_parameter', 'rom_data_creator', 'create_journal_file',
         'list_rom_parameter', 'delete_rom_parameter']

    _child_classes = dict(
        rom_type=rom_type_cls,
        transient_setup=transient_setup_cls,
        file_saving_frequency=file_saving_frequency_cls,
        joule_heat_parameter=joule_heat_parameter_cls,
        add_rom_parameter=add_rom_parameter_cls,
        rom_data_creator=rom_data_creator_cls,
        create_journal_file=create_journal_file_cls,
        list_rom_parameter=list_rom_parameter_cls,
        delete_rom_parameter=delete_rom_parameter_cls,
    )

