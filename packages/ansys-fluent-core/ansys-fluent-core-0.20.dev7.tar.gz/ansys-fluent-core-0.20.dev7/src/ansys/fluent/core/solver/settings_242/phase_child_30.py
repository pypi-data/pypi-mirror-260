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

from .momentum_11 import momentum as momentum_cls
from .turbulence_6 import turbulence as turbulence_cls
from .thermal_6 import thermal as thermal_cls
from .radiation_6 import radiation as radiation_cls
from .species_10 import species as species_cls
from .dpm_3 import dpm as dpm_cls
from .multiphase_7 import multiphase as multiphase_cls
from .potential_3 import potential as potential_cls
from .structure_1 import structure as structure_cls
from .uds_1 import uds as uds_cls
from .icing_2 import icing as icing_cls
from .ablation_1 import ablation as ablation_cls
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
         'multiphase', 'potential', 'structure', 'uds', 'icing', 'ablation',
         'geometry']

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
        ablation=ablation_cls,
        geometry=geometry_cls,
        adjacent_cell_zone=adjacent_cell_zone_cls,
        shadow_face_zone=shadow_face_zone_cls,
    )

