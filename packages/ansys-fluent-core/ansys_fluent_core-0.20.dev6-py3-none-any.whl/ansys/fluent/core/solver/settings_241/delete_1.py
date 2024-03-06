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

from .name_list import name_list as name_list_cls
class delete(CommandWithPositionalArgs):
    """
    Delete selected objects.
    
    Parameters
    ----------
        name_list : typing.List[str]
            Select objects to be deleted.
    
    """

    fluent_name = "delete"

    argument_names = \
        ['name_list']

    _child_classes = dict(
        name_list=name_list_cls,
    )

