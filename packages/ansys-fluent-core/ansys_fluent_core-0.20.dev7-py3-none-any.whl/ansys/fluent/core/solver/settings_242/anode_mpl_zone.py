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

from .anode_mpl_zone_list import anode_mpl_zone_list as anode_mpl_zone_list_cls
from .anode_mpl_update import anode_mpl_update as anode_mpl_update_cls
from .anode_mpl_material import anode_mpl_material as anode_mpl_material_cls
from .anode_mpl_porosity import anode_mpl_porosity as anode_mpl_porosity_cls
from .anode_mpl_permeability import anode_mpl_permeability as anode_mpl_permeability_cls
from .anode_mpl_angle import anode_mpl_angle as anode_mpl_angle_cls
from .anode_mpl_angle_hi import anode_mpl_angle_hi as anode_mpl_angle_hi_cls
from .anode_mpl_fraction import anode_mpl_fraction as anode_mpl_fraction_cls
from .anode_mpl_a import anode_mpl_a as anode_mpl_a_cls
from .anode_mpl_b import anode_mpl_b as anode_mpl_b_cls
from .anode_mpl_c import anode_mpl_c as anode_mpl_c_cls
from .anode_mpl_condensation import anode_mpl_condensation as anode_mpl_condensation_cls
from .anode_mpl_evaporation import anode_mpl_evaporation as anode_mpl_evaporation_cls
from .anode_mpl_poresize import anode_mpl_poresize as anode_mpl_poresize_cls
class anode_mpl_zone(Group):
    """
    Set up anode MPL.
    """

    fluent_name = "anode-mpl-zone"

    child_names = \
        ['anode_mpl_zone_list', 'anode_mpl_update', 'anode_mpl_material',
         'anode_mpl_porosity', 'anode_mpl_permeability', 'anode_mpl_angle',
         'anode_mpl_angle_hi', 'anode_mpl_fraction', 'anode_mpl_a',
         'anode_mpl_b', 'anode_mpl_c', 'anode_mpl_condensation',
         'anode_mpl_evaporation', 'anode_mpl_poresize']

    _child_classes = dict(
        anode_mpl_zone_list=anode_mpl_zone_list_cls,
        anode_mpl_update=anode_mpl_update_cls,
        anode_mpl_material=anode_mpl_material_cls,
        anode_mpl_porosity=anode_mpl_porosity_cls,
        anode_mpl_permeability=anode_mpl_permeability_cls,
        anode_mpl_angle=anode_mpl_angle_cls,
        anode_mpl_angle_hi=anode_mpl_angle_hi_cls,
        anode_mpl_fraction=anode_mpl_fraction_cls,
        anode_mpl_a=anode_mpl_a_cls,
        anode_mpl_b=anode_mpl_b_cls,
        anode_mpl_c=anode_mpl_c_cls,
        anode_mpl_condensation=anode_mpl_condensation_cls,
        anode_mpl_evaporation=anode_mpl_evaporation_cls,
        anode_mpl_poresize=anode_mpl_poresize_cls,
    )

