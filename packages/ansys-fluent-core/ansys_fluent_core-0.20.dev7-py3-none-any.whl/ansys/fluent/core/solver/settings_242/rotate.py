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

from .angle import angle as angle_cls
from .origin import origin as origin_cls
from .axis_components import axis_components as axis_components_cls
class rotate(Command):
    """
    Rotate the mesh.
    
    Parameters
    ----------
        angle : real
            'angle' child.
        origin : typing.List[real]
            'origin' child.
        axis_components : typing.List[real]
            'axis_components' child.
    
    """

    fluent_name = "rotate"

    argument_names = \
        ['angle', 'origin', 'axis_components']

    _child_classes = dict(
        angle=angle_cls,
        origin=origin_cls,
        axis_components=axis_components_cls,
    )

