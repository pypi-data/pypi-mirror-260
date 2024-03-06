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
from .phase_6 import phase as phase_cls
from .momentum_2 import momentum as momentum_cls
from .turbulence_1 import turbulence as turbulence_cls
from .thermal_1 import thermal as thermal_cls
from .radiation_2 import radiation as radiation_cls
from .species_6 import species as species_cls
from .dpm import dpm as dpm_cls
from .multiphase_3 import multiphase as multiphase_cls
from .potential_1 import potential as potential_cls
from .structure_1 import structure as structure_cls
from .uds_1 import uds as uds_cls
from .icing_1 import icing as icing_cls
from .geometry_2 import geometry as geometry_cls
class intake_fan_child(Group):
    """
    'child_object_type' of intake_fan.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'momentum', 'turbulence', 'thermal', 'radiation',
         'species', 'dpm', 'multiphase', 'potential', 'structure', 'uds',
         'icing', 'geometry']

    _child_classes = dict(
        name=name_cls,
        phase=phase_cls,
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

