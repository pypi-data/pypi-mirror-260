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

from .type_1 import type as type_cls
from .name_1 import name as name_cls
class copy_by_name(Command):
    """
    Copy a material from the database (pick by name).
    
    Parameters
    ----------
        type : str
            'type' child.
        name : str
            'name' child.
    
    """

    fluent_name = "copy-by-name"

    argument_names = \
        ['type', 'name']

    _child_classes = dict(
        type=type_cls,
        name=name_cls,
    )

