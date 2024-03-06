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

from .momentum_3 import momentum as momentum_cls
from .turbulence_2 import turbulence as turbulence_cls
from .thermal_2 import thermal as thermal_cls
from .radiation_3 import radiation as radiation_cls
from .species_7 import species as species_cls
from .dpm_1 import dpm as dpm_cls
from .multiphase_4 import multiphase as multiphase_cls
from .potential_1 import potential as potential_cls
from .structure_1 import structure as structure_cls
from .uds_1 import uds as uds_cls
from .icing_1 import icing as icing_cls
from .geometry_3 import geometry as geometry_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['momentum', 'turbulence', 'thermal', 'radiation', 'species', 'dpm',
         'multiphase', 'potential', 'structure', 'uds', 'icing', 'geometry']

    query_names = \
        ['adjacent_cell_zone', 'shadow_face_zone']

    _child_classes = dict(
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
        adjacent_cell_zone=adjacent_cell_zone_cls,
        shadow_face_zone=shadow_face_zone_cls,
    )

