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

from .file_name_1 import file_name as file_name_cls
from .pdf_file_name import pdf_file_name as pdf_file_name_cls
class read_case_data(Command):
    """
    'read_case_data' command.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        pdf_file_name : str
            'pdf_file_name' child.
    
    """

    fluent_name = "read-case-data"

    argument_names = \
        ['file_name', 'pdf_file_name']

    _child_classes = dict(
        file_name=file_name_cls,
        pdf_file_name=pdf_file_name_cls,
    )

