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

from .anode_gdl_zone_list import anode_gdl_zone_list as anode_gdl_zone_list_cls
from .anode_gdl_update import anode_gdl_update as anode_gdl_update_cls
from .anode_gdl_material import anode_gdl_material as anode_gdl_material_cls
from .anode_gdl_porosity import anode_gdl_porosity as anode_gdl_porosity_cls
from .anode_gdl_permeability import anode_gdl_permeability as anode_gdl_permeability_cls
from .anode_gdl_angle import anode_gdl_angle as anode_gdl_angle_cls
from .anode_gdl_angle_hi import anode_gdl_angle_hi as anode_gdl_angle_hi_cls
from .anode_gdl_fraction import anode_gdl_fraction as anode_gdl_fraction_cls
from .anode_gdl_waterremoval import anode_gdl_waterremoval as anode_gdl_waterremoval_cls
from .anode_gdl_a import anode_gdl_a as anode_gdl_a_cls
from .anode_gdl_b import anode_gdl_b as anode_gdl_b_cls
from .anode_gdl_c import anode_gdl_c as anode_gdl_c_cls
from .anode_gdl_condensation import anode_gdl_condensation as anode_gdl_condensation_cls
from .anode_gdl_evaporation import anode_gdl_evaporation as anode_gdl_evaporation_cls
from .anode_gdl_poresize import anode_gdl_poresize as anode_gdl_poresize_cls
class anode_gdl_zone(Group):
    """
    Set up anode GDL.
    """

    fluent_name = "anode-gdl-zone"

    child_names = \
        ['anode_gdl_zone_list', 'anode_gdl_update', 'anode_gdl_material',
         'anode_gdl_porosity', 'anode_gdl_permeability', 'anode_gdl_angle',
         'anode_gdl_angle_hi', 'anode_gdl_fraction', 'anode_gdl_waterremoval',
         'anode_gdl_a', 'anode_gdl_b', 'anode_gdl_c',
         'anode_gdl_condensation', 'anode_gdl_evaporation',
         'anode_gdl_poresize']

    _child_classes = dict(
        anode_gdl_zone_list=anode_gdl_zone_list_cls,
        anode_gdl_update=anode_gdl_update_cls,
        anode_gdl_material=anode_gdl_material_cls,
        anode_gdl_porosity=anode_gdl_porosity_cls,
        anode_gdl_permeability=anode_gdl_permeability_cls,
        anode_gdl_angle=anode_gdl_angle_cls,
        anode_gdl_angle_hi=anode_gdl_angle_hi_cls,
        anode_gdl_fraction=anode_gdl_fraction_cls,
        anode_gdl_waterremoval=anode_gdl_waterremoval_cls,
        anode_gdl_a=anode_gdl_a_cls,
        anode_gdl_b=anode_gdl_b_cls,
        anode_gdl_c=anode_gdl_c_cls,
        anode_gdl_condensation=anode_gdl_condensation_cls,
        anode_gdl_evaporation=anode_gdl_evaporation_cls,
        anode_gdl_poresize=anode_gdl_poresize_cls,
    )

