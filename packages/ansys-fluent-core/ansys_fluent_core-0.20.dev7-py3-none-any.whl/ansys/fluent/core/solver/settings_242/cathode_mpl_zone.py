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

from .cathode_mpl_zone_list import cathode_mpl_zone_list as cathode_mpl_zone_list_cls
from .cathode_mpl_update import cathode_mpl_update as cathode_mpl_update_cls
from .cathode_mpl_material import cathode_mpl_material as cathode_mpl_material_cls
from .cathode_mpl_porosity import cathode_mpl_porosity as cathode_mpl_porosity_cls
from .cathode_mpl_permeability import cathode_mpl_permeability as cathode_mpl_permeability_cls
from .cathode_mpl_angle import cathode_mpl_angle as cathode_mpl_angle_cls
from .cathode_mpl_angle_hi import cathode_mpl_angle_hi as cathode_mpl_angle_hi_cls
from .cathode_mpl_fraction import cathode_mpl_fraction as cathode_mpl_fraction_cls
from .cathode_mpl_a import cathode_mpl_a as cathode_mpl_a_cls
from .cathode_mpl_b import cathode_mpl_b as cathode_mpl_b_cls
from .cathode_mpl_c import cathode_mpl_c as cathode_mpl_c_cls
from .cathode_mpl_condensation import cathode_mpl_condensation as cathode_mpl_condensation_cls
from .cathode_mpl_evaporation import cathode_mpl_evaporation as cathode_mpl_evaporation_cls
from .cathode_mpl_poresize import cathode_mpl_poresize as cathode_mpl_poresize_cls
class cathode_mpl_zone(Group):
    """
    Set up cathode MPL.
    """

    fluent_name = "cathode-mpl-zone"

    child_names = \
        ['cathode_mpl_zone_list', 'cathode_mpl_update',
         'cathode_mpl_material', 'cathode_mpl_porosity',
         'cathode_mpl_permeability', 'cathode_mpl_angle',
         'cathode_mpl_angle_hi', 'cathode_mpl_fraction', 'cathode_mpl_a',
         'cathode_mpl_b', 'cathode_mpl_c', 'cathode_mpl_condensation',
         'cathode_mpl_evaporation', 'cathode_mpl_poresize']

    _child_classes = dict(
        cathode_mpl_zone_list=cathode_mpl_zone_list_cls,
        cathode_mpl_update=cathode_mpl_update_cls,
        cathode_mpl_material=cathode_mpl_material_cls,
        cathode_mpl_porosity=cathode_mpl_porosity_cls,
        cathode_mpl_permeability=cathode_mpl_permeability_cls,
        cathode_mpl_angle=cathode_mpl_angle_cls,
        cathode_mpl_angle_hi=cathode_mpl_angle_hi_cls,
        cathode_mpl_fraction=cathode_mpl_fraction_cls,
        cathode_mpl_a=cathode_mpl_a_cls,
        cathode_mpl_b=cathode_mpl_b_cls,
        cathode_mpl_c=cathode_mpl_c_cls,
        cathode_mpl_condensation=cathode_mpl_condensation_cls,
        cathode_mpl_evaporation=cathode_mpl_evaporation_cls,
        cathode_mpl_poresize=cathode_mpl_poresize_cls,
    )

