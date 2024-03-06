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

from .state_name import state_name as state_name_cls
class copy(Command):
    """
    Create a new display state with settings copied from an existing display state.
    
    Parameters
    ----------
        state_name : str
            'state_name' child.
    
    """

    fluent_name = "copy"

    argument_names = \
        ['state_name']

    _child_classes = dict(
        state_name=state_name_cls,
    )

