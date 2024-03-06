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

from .name import name as name_cls
from .phase_10 import phase as phase_cls
from .flow_direction import flow_direction as flow_direction_cls
from .direction_vector import direction_vector as direction_vector_cls
from .axis_direction_2 import axis_direction as axis_direction_cls
from .axis_origin_2 import axis_origin as axis_origin_cls
from .momentum_4 import momentum as momentum_cls
from .turbulence_3 import turbulence as turbulence_cls
from .thermal_3 import thermal as thermal_cls
from .radiation_3 import radiation as radiation_cls
from .species_8 import species as species_cls
from .dpm_1 import dpm as dpm_cls
from .multiphase_5 import multiphase as multiphase_cls
from .potential_2 import potential as potential_cls
from .structure_1 import structure as structure_cls
from .uds_1 import uds as uds_cls
from .icing_1 import icing as icing_cls
from .geometry_2 import geometry as geometry_cls
class mass_flow_outlet_child(Group):
    """
    'child_object_type' of mass_flow_outlet.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'flow_direction', 'direction_vector',
         'axis_direction', 'axis_origin', 'momentum', 'turbulence', 'thermal',
         'radiation', 'species', 'dpm', 'multiphase', 'potential',
         'structure', 'uds', 'icing', 'geometry']

    _child_classes = dict(
        name=name_cls,
        phase=phase_cls,
        flow_direction=flow_direction_cls,
        direction_vector=direction_vector_cls,
        axis_direction=axis_direction_cls,
        axis_origin=axis_origin_cls,
        momentum=momentum_cls,
        turbulence=turbulence_cls,
        thermal=thermal_cls,
        radiation=radiation_cls,
        species=species_cls,
        dpm=dpm_cls,
        multiphase=multiphase_cls,
        potential=potential_cls,
        structure=structure_cls,
        uds=uds_cls,
        icing=icing_cls,
        geometry=geometry_cls,
    )

