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
from .in_ import in_ as in__cls
class dolly(Command):
    """
    Adjust the camera position and target.
    
    Parameters
    ----------
        right : real
            'right' child.
        up : real
            'up' child.
        in_ : real
            'in' child.
    
    """

    fluent_name = "dolly"

    argument_names = \
        ['right', 'up', 'in_']

    _child_classes = dict(
        right=right_cls,
        up=up_cls,
        in_=in__cls,
    )

