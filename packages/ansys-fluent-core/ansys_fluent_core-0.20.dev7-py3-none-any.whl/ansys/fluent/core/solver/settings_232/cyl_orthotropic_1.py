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

from .axis_origin import axis_origin as axis_origin_cls
from .axis_direction import axis_direction as axis_direction_cls
from .radial_conductivity import radial_conductivity as radial_conductivity_cls
from .tangential_conductivity import tangential_conductivity as tangential_conductivity_cls
from .axial_conductivity import axial_conductivity as axial_conductivity_cls
class cyl_orthotropic(Group):
    """
    'cyl_orthotropic' child.
    """

    fluent_name = "cyl-orthotropic"

    child_names = \
        ['axis_origin', 'axis_direction', 'radial_conductivity',
         'tangential_conductivity', 'axial_conductivity']

    _child_classes = dict(
        axis_origin=axis_origin_cls,
        axis_direction=axis_direction_cls,
        radial_conductivity=radial_conductivity_cls,
        tangential_conductivity=tangential_conductivity_cls,
        axial_conductivity=axial_conductivity_cls,
    )

