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

from .name_1 import name as name_cls
class delete(CommandWithPositionalArgs):
    """
    Delete a mesh interface.
    
    Parameters
    ----------
        name : str
            'name' child.
    
    """

    fluent_name = "delete"

    argument_names = \
        ['name']

    _child_classes = dict(
        name=name_cls,
    )

