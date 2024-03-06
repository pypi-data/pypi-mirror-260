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

from .database import database as database_cls
from .fluid import fluid as fluid_cls
from .solid import solid as solid_cls
from .mixture import mixture as mixture_cls
from .inert_particle import inert_particle as inert_particle_cls
from .droplet_particle import droplet_particle as droplet_particle_cls
from .combusting_particle import combusting_particle as combusting_particle_cls
from .particle_mixture import particle_mixture as particle_mixture_cls
from .list_materials_1 import list_materials as list_materials_cls
from .list_properties_3 import list_properties as list_properties_cls
class materials(Group):
    """
    'materials' child.
    """

    fluent_name = "materials"

    child_names = \
        ['database', 'fluid', 'solid', 'mixture', 'inert_particle',
         'droplet_particle', 'combusting_particle', 'particle_mixture']

    command_names = \
        ['list_materials', 'list_properties']

    _child_classes = dict(
        database=database_cls,
        fluid=fluid_cls,
        solid=solid_cls,
        mixture=mixture_cls,
        inert_particle=inert_particle_cls,
        droplet_particle=droplet_particle_cls,
        combusting_particle=combusting_particle_cls,
        particle_mixture=particle_mixture_cls,
        list_materials=list_materials_cls,
        list_properties=list_properties_cls,
    )

