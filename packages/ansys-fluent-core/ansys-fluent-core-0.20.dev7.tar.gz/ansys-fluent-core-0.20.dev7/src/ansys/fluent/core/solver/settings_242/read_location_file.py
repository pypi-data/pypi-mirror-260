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

from .file_name_1_7 import file_name_1 as file_name_1_cls
class read_location_file(Command):
    """
    Command object to read location file in the pack builder.
    
    Parameters
    ----------
        file_name_1 : str
            Module Location file name with its full path.
    
    """

    fluent_name = "read-location-file"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_1_cls,
    )

