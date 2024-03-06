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

from .fluid import fluid as fluid_cls
from .solid import solid as solid_cls
from .mixture import mixture as mixture_cls
from .inert_particle import inert_particle as inert_particle_cls
from .droplet_particle import droplet_particle as droplet_particle_cls
from .combusting_particle import combusting_particle as combusting_particle_cls
from .particle_mixture import particle_mixture as particle_mixture_cls
from .list_materials import list_materials as list_materials_cls
from .copy_database_material_by_name import copy_database_material_by_name as copy_database_material_by_name_cls
from .copy_database_material_by_formula import copy_database_material_by_formula as copy_database_material_by_formula_cls
class materials(Group):
    """
    'materials' child.
    """

    fluent_name = "materials"

    child_names = \
        ['fluid', 'solid', 'mixture', 'inert_particle', 'droplet_particle',
         'combusting_particle', 'particle_mixture']

    command_names = \
        ['list_materials', 'copy_database_material_by_name',
         'copy_database_material_by_formula']

    _child_classes = dict(
        fluid=fluid_cls,
        solid=solid_cls,
        mixture=mixture_cls,
        inert_particle=inert_particle_cls,
        droplet_particle=droplet_particle_cls,
        combusting_particle=combusting_particle_cls,
        particle_mixture=particle_mixture_cls,
        list_materials=list_materials_cls,
        copy_database_material_by_name=copy_database_material_by_name_cls,
        copy_database_material_by_formula=copy_database_material_by_formula_cls,
    )

