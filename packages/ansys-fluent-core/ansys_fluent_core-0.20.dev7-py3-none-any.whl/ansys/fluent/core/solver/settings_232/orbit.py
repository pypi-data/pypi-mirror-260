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

from .right import right as right_cls
from .up import up as up_cls
class orbit(Command):
    """
    Adjust the camera position without modifying the target.
    
    Parameters
    ----------
        right : real
            'right' child.
        up : real
            'up' child.
    
    """

    fluent_name = "orbit"

    argument_names = \
        ['right', 'up']

    _child_classes = dict(
        right=right_cls,
        up=up_cls,
    )

