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

from .mem_zone import mem_zone as mem_zone_cls
from .species_permeation import species_permeation as species_permeation_cls
from .mem_anode_interface import mem_anode_interface as mem_anode_interface_cls
from .mem_cathode_interface import mem_cathode_interface as mem_cathode_interface_cls
from .mem_thickness import mem_thickness as mem_thickness_cls
from .mem_cond import mem_cond as mem_cond_cls
class electrolyte(Group):
    """
    'electrolyte' child.
    """

    fluent_name = "electrolyte"

    child_names = \
        ['mem_zone', 'species_permeation', 'mem_anode_interface',
         'mem_cathode_interface', 'mem_thickness', 'mem_cond']

    _child_classes = dict(
        mem_zone=mem_zone_cls,
        species_permeation=species_permeation_cls,
        mem_anode_interface=mem_anode_interface_cls,
        mem_cathode_interface=mem_cathode_interface_cls,
        mem_thickness=mem_thickness_cls,
        mem_cond=mem_cond_cls,
    )

