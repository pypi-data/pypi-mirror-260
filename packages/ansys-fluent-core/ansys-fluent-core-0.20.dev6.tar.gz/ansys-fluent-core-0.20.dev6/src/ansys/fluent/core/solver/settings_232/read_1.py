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

from .file_type import file_type as file_type_cls
from .file_name_1 import file_name as file_name_cls
from .pdf_file_name import pdf_file_name as pdf_file_name_cls
from .lightweight_setup import lightweight_setup as lightweight_setup_cls
class read(Command):
    """
    'read' command.
    
    Parameters
    ----------
        file_type : str
            'file_type' child.
        file_name : str
            'file_name' child.
        pdf_file_name : str
            'pdf_file_name' child.
        lightweight_setup : bool
            'lightweight_setup' child.
    
    """

    fluent_name = "read"

    argument_names = \
        ['file_type', 'file_name', 'pdf_file_name', 'lightweight_setup']

    _child_classes = dict(
        file_type=file_type_cls,
        file_name=file_name_cls,
        pdf_file_name=pdf_file_name_cls,
        lightweight_setup=lightweight_setup_cls,
    )

