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

from .type_2 import type as type_cls
class projection(Command):
    """
    Set the camera projection.
    
    Parameters
    ----------
        type : str
            'type' child.
    
    """

    fluent_name = "projection"

    argument_names = \
        ['type']

    _child_classes = dict(
        type=type_cls,
    )

