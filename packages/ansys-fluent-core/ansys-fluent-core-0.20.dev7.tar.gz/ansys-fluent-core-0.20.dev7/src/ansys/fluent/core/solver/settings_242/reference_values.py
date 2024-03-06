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

from .area_1 import area as area_cls
from .depth import depth as depth_cls
from .density_6 import density as density_cls
from .enthalpy import enthalpy as enthalpy_cls
from .length_1 import length as length_cls
from .pressure import pressure as pressure_cls
from .temperature_4 import temperature as temperature_cls
from .yplus import yplus as yplus_cls
from .velocity_3 import velocity as velocity_cls
from .viscosity_3 import viscosity as viscosity_cls
from .ratio_of_specific_heats import ratio_of_specific_heats as ratio_of_specific_heats_cls
from .zone import zone as zone_cls
from .compute import compute as compute_cls
from .list_values import list_values as list_values_cls
class reference_values(Group):
    """
    'reference_values' child.
    """

    fluent_name = "reference-values"

    child_names = \
        ['area', 'depth', 'density', 'enthalpy', 'length', 'pressure',
         'temperature', 'yplus', 'velocity', 'viscosity',
         'ratio_of_specific_heats', 'zone']

    command_names = \
        ['compute', 'list_values']

    _child_classes = dict(
        area=area_cls,
        depth=depth_cls,
        density=density_cls,
        enthalpy=enthalpy_cls,
        length=length_cls,
        pressure=pressure_cls,
        temperature=temperature_cls,
        yplus=yplus_cls,
        velocity=velocity_cls,
        viscosity=viscosity_cls,
        ratio_of_specific_heats=ratio_of_specific_heats_cls,
        zone=zone_cls,
        compute=compute_cls,
        list_values=list_values_cls,
    )

