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

from .command_name import command_name as command_name_cls
class enable(Command):
    """
    Enable an execute-command.
    
    Parameters
    ----------
        command_name : str
            'command_name' child.
    
    """

    fluent_name = "enable"

    argument_names = \
        ['command_name']

    _child_classes = dict(
        command_name=command_name_cls,
    )

