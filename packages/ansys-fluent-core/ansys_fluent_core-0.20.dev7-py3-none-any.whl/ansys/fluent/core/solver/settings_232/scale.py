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

from .x_scale import x_scale as x_scale_cls
from .y_scale import y_scale as y_scale_cls
from .z_scale import z_scale as z_scale_cls
class scale(Command):
    """
    'scale' command.
    
    Parameters
    ----------
        x_scale : real
            'x_scale' child.
        y_scale : real
            'y_scale' child.
        z_scale : real
            'z_scale' child.
    
    """

    fluent_name = "scale"

    argument_names = \
        ['x_scale', 'y_scale', 'z_scale']

    _child_classes = dict(
        x_scale=x_scale_cls,
        y_scale=y_scale_cls,
        z_scale=z_scale_cls,
    )

