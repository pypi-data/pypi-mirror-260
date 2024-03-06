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

from .enabled_17 import enabled as enabled_cls
from .cell_type import cell_type as cell_type_cls
from .cyl_axis_vec import cyl_axis_vec as cyl_axis_vec_cls
from .prism_axis_vec import prism_axis_vec as prism_axis_vec_cls
from .prism_vec2 import prism_vec2 as prism_vec2_cls
from .pouch_normal_vec import pouch_normal_vec as pouch_normal_vec_cls
from .thermal_conductivity import thermal_conductivity as thermal_conductivity_cls
class orthotropic_k(Group):
    """
    Set parameters related to orthotropic thermal conductivity.
    """

    fluent_name = "orthotropic-k"

    child_names = \
        ['enabled', 'cell_type', 'cyl_axis_vec', 'prism_axis_vec',
         'prism_vec2', 'pouch_normal_vec', 'thermal_conductivity']

    _child_classes = dict(
        enabled=enabled_cls,
        cell_type=cell_type_cls,
        cyl_axis_vec=cyl_axis_vec_cls,
        prism_axis_vec=prism_axis_vec_cls,
        prism_vec2=prism_vec2_cls,
        pouch_normal_vec=pouch_normal_vec_cls,
        thermal_conductivity=thermal_conductivity_cls,
    )

