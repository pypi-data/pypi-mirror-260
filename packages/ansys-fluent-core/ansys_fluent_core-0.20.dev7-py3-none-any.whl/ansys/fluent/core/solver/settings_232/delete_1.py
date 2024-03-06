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

from .si_delete import si_delete as si_delete_cls
class delete(CommandWithPositionalArgs):
    """
    Delete a mesh interface.
    
    Parameters
    ----------
        si_delete : str
            'si_delete' child.
    
    """

    fluent_name = "delete"

    argument_names = \
        ['si_delete']

    _child_classes = dict(
        si_delete=si_delete_cls,
    )

