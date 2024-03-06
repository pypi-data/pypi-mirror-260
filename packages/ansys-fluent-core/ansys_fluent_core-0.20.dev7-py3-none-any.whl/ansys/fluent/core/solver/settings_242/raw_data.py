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

from .import_files_enabled import import_files_enabled as import_files_enabled_cls
from .number_of_files import number_of_files as number_of_files_cls
from .files import files as files_cls
from .capacify_fade_enabled import capacify_fade_enabled as capacify_fade_enabled_cls
class raw_data(Command):
    """
    Specify U and Y parameters using raw data.
    
    Parameters
    ----------
        import_files_enabled : bool
            Import raw data in the NTGK model.
        number_of_files : int
            Total number of discharging files.
        files : typing.List[str]
            Discharging file names in the NTGK model.
        capacify_fade_enabled : bool
            Enable capacity fade model in the NTGK model.
    
    """

    fluent_name = "raw-data"

    argument_names = \
        ['import_files_enabled', 'number_of_files', 'files',
         'capacify_fade_enabled']

    _child_classes = dict(
        import_files_enabled=import_files_enabled_cls,
        number_of_files=number_of_files_cls,
        files=files_cls,
        capacify_fade_enabled=capacify_fade_enabled_cls,
    )

