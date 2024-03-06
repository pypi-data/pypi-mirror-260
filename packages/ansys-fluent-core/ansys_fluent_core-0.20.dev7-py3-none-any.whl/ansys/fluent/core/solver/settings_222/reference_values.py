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

from .area import area as area_cls
from .compute_1 import compute as compute_cls
from .depth import depth as depth_cls
from .density_1 import density as density_cls
from .enthalpy import enthalpy as enthalpy_cls
from .length_val import length_val as length_val_cls
from .pressure import pressure as pressure_cls
from .temperature_1 import temperature as temperature_cls
from .yplus import yplus as yplus_cls
from .velocity import velocity as velocity_cls
from .viscosity_1 import viscosity as viscosity_cls
from .list_val import list_val as list_val_cls
class reference_values(Group):
    """
    'reference_values' child.
    """

    fluent_name = "reference-values"

    child_names = \
        ['area', 'compute', 'depth', 'density', 'enthalpy', 'length_val',
         'pressure', 'temperature', 'yplus', 'velocity', 'viscosity',
         'list_val']

    _child_classes = dict(
        area=area_cls,
        compute=compute_cls,
        depth=depth_cls,
        density=density_cls,
        enthalpy=enthalpy_cls,
        length_val=length_val_cls,
        pressure=pressure_cls,
        temperature=temperature_cls,
        yplus=yplus_cls,
        velocity=velocity_cls,
        viscosity=viscosity_cls,
        list_val=list_val_cls,
    )

