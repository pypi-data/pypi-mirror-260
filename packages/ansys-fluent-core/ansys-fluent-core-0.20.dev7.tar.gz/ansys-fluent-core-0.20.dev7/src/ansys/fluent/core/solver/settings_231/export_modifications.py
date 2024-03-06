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

from .command_list import command_list as command_list_cls
from .filename import filename as filename_cls
class export_modifications(Command):
    """
    Export all case modifications to a tsv file.
    
    Parameters
    ----------
        command_list : typing.List[str]
            'command_list' child.
        filename : str
            'filename' child.
    
    """

    fluent_name = "export-modifications"

    argument_names = \
        ['command_list', 'filename']

    _child_classes = dict(
        command_list=command_list_cls,
        filename=filename_cls,
    )

