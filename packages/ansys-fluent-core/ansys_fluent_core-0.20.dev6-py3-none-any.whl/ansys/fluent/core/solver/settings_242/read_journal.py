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

from .file_name_list import file_name_list as file_name_list_cls
class read_journal(Command):
    """
    Read a journal file.
    
    Parameters
    ----------
        file_name_list : typing.List[str]
            'file_name_list' child.
    
    """

    fluent_name = "read-journal"

    argument_names = \
        ['file_name_list']

    _child_classes = dict(
        file_name_list=file_name_list_cls,
    )

