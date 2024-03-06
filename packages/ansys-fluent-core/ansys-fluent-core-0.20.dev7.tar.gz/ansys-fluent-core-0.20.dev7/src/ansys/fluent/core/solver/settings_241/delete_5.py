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

from .delete_all_1 import delete_all as delete_all_cls
from .name_5 import name as name_cls
class delete(CommandWithPositionalArgs):
    """
    Delete animation sequence.
    
    Parameters
    ----------
        delete_all : bool
            Yes: "Delete all animations", no: "Delete single animation.".
        name : str
            Select animation to delete.
    
    """

    fluent_name = "delete"

    argument_names = \
        ['delete_all', 'name']

    _child_classes = dict(
        delete_all=delete_all_cls,
        name=name_cls,
    )

