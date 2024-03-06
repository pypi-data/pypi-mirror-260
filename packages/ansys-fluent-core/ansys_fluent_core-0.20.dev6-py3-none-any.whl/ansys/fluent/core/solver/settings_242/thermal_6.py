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

from .wall_thickness_old import wall_thickness_old as wall_thickness_old_cls
from .wall_thickness import wall_thickness as wall_thickness_cls
from .q_dot import q_dot as q_dot_cls
from .material_1 import material as material_cls
from .thermal_bc import thermal_bc as thermal_bc_cls
from .t import t as t_cls
from .q import q as q_cls
from .h_1 import h as h_cls
from .tinf import tinf as tinf_cls
from .planar_conduction import planar_conduction as planar_conduction_cls
from .shell_conduction import shell_conduction as shell_conduction_cls
from .thin_wall import thin_wall as thin_wall_cls
from .internal_emissivity import internal_emissivity as internal_emissivity_cls
from .external_emissivity import external_emissivity as external_emissivity_cls
from .trad import trad as trad_cls
from .int_rad import int_rad as int_rad_cls
from .trad_internal import trad_internal as trad_internal_cls
from .area_enhancement_factor import area_enhancement_factor as area_enhancement_factor_cls
from .contact_resistance_1 import contact_resistance as contact_resistance_cls
from .therm_accom_coef import therm_accom_coef as therm_accom_coef_cls
from .eve_accom_coef import eve_accom_coef as eve_accom_coef_cls
from .caf import caf as caf_cls
from .thermal_stabilization import thermal_stabilization as thermal_stabilization_cls
from .scale_factor_1 import scale_factor as scale_factor_cls
from .stab_method import stab_method as stab_method_cls
from .boundary_advection import boundary_advection as boundary_advection_cls
class thermal(Group):
    """
    Help not available.
    """

    fluent_name = "thermal"

    child_names = \
        ['wall_thickness_old', 'wall_thickness', 'q_dot', 'material',
         'thermal_bc', 't', 'q', 'h', 'tinf', 'planar_conduction',
         'shell_conduction', 'thin_wall', 'internal_emissivity',
         'external_emissivity', 'trad', 'int_rad', 'trad_internal',
         'area_enhancement_factor', 'contact_resistance', 'therm_accom_coef',
         'eve_accom_coef', 'caf', 'thermal_stabilization', 'scale_factor',
         'stab_method', 'boundary_advection']

    _child_classes = dict(
        wall_thickness_old=wall_thickness_old_cls,
        wall_thickness=wall_thickness_cls,
        q_dot=q_dot_cls,
        material=material_cls,
        thermal_bc=thermal_bc_cls,
        t=t_cls,
        q=q_cls,
        h=h_cls,
        tinf=tinf_cls,
        planar_conduction=planar_conduction_cls,
        shell_conduction=shell_conduction_cls,
        thin_wall=thin_wall_cls,
        internal_emissivity=internal_emissivity_cls,
        external_emissivity=external_emissivity_cls,
        trad=trad_cls,
        int_rad=int_rad_cls,
        trad_internal=trad_internal_cls,
        area_enhancement_factor=area_enhancement_factor_cls,
        contact_resistance=contact_resistance_cls,
        therm_accom_coef=therm_accom_coef_cls,
        eve_accom_coef=eve_accom_coef_cls,
        caf=caf_cls,
        thermal_stabilization=thermal_stabilization_cls,
        scale_factor=scale_factor_cls,
        stab_method=stab_method_cls,
        boundary_advection=boundary_advection_cls,
    )

