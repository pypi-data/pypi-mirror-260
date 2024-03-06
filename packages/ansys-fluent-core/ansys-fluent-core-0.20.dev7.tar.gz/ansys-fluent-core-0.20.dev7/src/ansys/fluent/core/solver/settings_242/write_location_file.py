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

from .file_name_9 import file_name as file_name_cls
class write_location_file(Command):
    """
    Command object to write location file in the pack builder.
    
    Parameters
    ----------
        file_name : str
            Write location information into a file in the pack builder.
    
    """

    fluent_name = "write-location-file"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

