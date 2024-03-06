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

from .file_name_11 import file_name as file_name_cls
from .frequency_4 import frequency as frequency_cls
from .max_files_1 import max_files as max_files_cls
class autosave(Command):
    """
    Menu for adjoint autosave.
    
    Parameters
    ----------
        file_name : str
            File name prefix for auto-saved files.
        frequency : int
            Autosave adjoint iteration frequency.
        max_files : int
            Maximum number of files retained.
    
    """

    fluent_name = "autosave"

    argument_names = \
        ['file_name', 'frequency', 'max_files']

    _child_classes = dict(
        file_name=file_name_cls,
        frequency=frequency_cls,
        max_files=max_files_cls,
    )

