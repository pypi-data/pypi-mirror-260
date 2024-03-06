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

from .width import width as width_cls
from .height import height as height_cls
class aspect_ratio(Command):
    """
    Set the aspect ratio of the active window.
    
    Parameters
    ----------
        width : real
            'width' child.
        height : real
            'height' child.
    
    """

    fluent_name = "aspect-ratio"

    argument_names = \
        ['width', 'height']

    _child_classes = dict(
        width=width_cls,
        height=height_cls,
    )

