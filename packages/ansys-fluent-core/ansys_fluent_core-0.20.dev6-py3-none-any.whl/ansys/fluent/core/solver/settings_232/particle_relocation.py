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

from .enhanced_cell_relocation_method import enhanced_cell_relocation_method as enhanced_cell_relocation_method_cls
from .load_legacy_particles import load_legacy_particles as load_legacy_particles_cls
from .overset_relocation_robustness_level import overset_relocation_robustness_level as overset_relocation_robustness_level_cls
from .legacy_particle_location_method_enabled import legacy_particle_location_method_enabled as legacy_particle_location_method_enabled_cls
class particle_relocation(Group):
    """
    Main menu holding information options to control relocating particles during case file reading or remeshing/adaption.
    """

    fluent_name = "particle-relocation"

    child_names = \
        ['enhanced_cell_relocation_method', 'load_legacy_particles',
         'overset_relocation_robustness_level',
         'legacy_particle_location_method_enabled']

    _child_classes = dict(
        enhanced_cell_relocation_method=enhanced_cell_relocation_method_cls,
        load_legacy_particles=load_legacy_particles_cls,
        overset_relocation_robustness_level=overset_relocation_robustness_level_cls,
        legacy_particle_location_method_enabled=legacy_particle_location_method_enabled_cls,
    )

