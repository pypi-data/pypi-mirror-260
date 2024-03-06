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

from .enabled_22 import enabled as enabled_cls
from .omega import omega as omega_cls
from .omega_pe import omega_pe as omega_pe_cls
from .omega_ne import omega_ne as omega_ne_cls
from .e_elastic_pe import e_elastic_pe as e_elastic_pe_cls
from .e_elastic_sp import e_elastic_sp as e_elastic_sp_cls
from .e_elastic_ne import e_elastic_ne as e_elastic_ne_cls
from .soc_ref import soc_ref as soc_ref_cls
from .cell_type_1 import cell_type as cell_type_cls
from .axis_vec import axis_vec as axis_vec_cls
from .origin_vec import origin_vec as origin_vec_cls
from .normal_vec import normal_vec as normal_vec_cls
from .prism_axis_vec_1 import prism_axis_vec as prism_axis_vec_cls
from .prism_vec2_1 import prism_vec2 as prism_vec2_cls
from .orientation_udf_name import orientation_udf_name as orientation_udf_name_cls
from .customize_swelling_strain_enabled import customize_swelling_strain_enabled as customize_swelling_strain_enabled_cls
from .strain_udf_name import strain_udf_name as strain_udf_name_cls
class swelling_model(Group):
    """
    Set battery swelling model related parameters.
    """

    fluent_name = "swelling-model"

    child_names = \
        ['enabled', 'omega', 'omega_pe', 'omega_ne', 'e_elastic_pe',
         'e_elastic_sp', 'e_elastic_ne', 'soc_ref', 'cell_type', 'axis_vec',
         'origin_vec', 'normal_vec', 'prism_axis_vec', 'prism_vec2',
         'orientation_udf_name', 'customize_swelling_strain_enabled',
         'strain_udf_name']

    _child_classes = dict(
        enabled=enabled_cls,
        omega=omega_cls,
        omega_pe=omega_pe_cls,
        omega_ne=omega_ne_cls,
        e_elastic_pe=e_elastic_pe_cls,
        e_elastic_sp=e_elastic_sp_cls,
        e_elastic_ne=e_elastic_ne_cls,
        soc_ref=soc_ref_cls,
        cell_type=cell_type_cls,
        axis_vec=axis_vec_cls,
        origin_vec=origin_vec_cls,
        normal_vec=normal_vec_cls,
        prism_axis_vec=prism_axis_vec_cls,
        prism_vec2=prism_vec2_cls,
        orientation_udf_name=orientation_udf_name_cls,
        customize_swelling_strain_enabled=customize_swelling_strain_enabled_cls,
        strain_udf_name=strain_udf_name_cls,
    )

