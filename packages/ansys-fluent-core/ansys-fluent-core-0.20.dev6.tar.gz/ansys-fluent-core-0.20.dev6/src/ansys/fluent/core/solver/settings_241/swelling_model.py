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

from .enabled_12 import enabled as enabled_cls
from .soc_ref import soc_ref as soc_ref_cls
from .cell_type import cell_type as cell_type_cls
from .axis_vec import axis_vec as axis_vec_cls
from .normal_vec import normal_vec as normal_vec_cls
from .prism_axis_vec import prism_axis_vec as prism_axis_vec_cls
from .prism_vec2 import prism_vec2 as prism_vec2_cls
from .orientation_udf_name import orientation_udf_name as orientation_udf_name_cls
from .customize_swelling_strain import customize_swelling_strain as customize_swelling_strain_cls
from .strain_udf_name import strain_udf_name as strain_udf_name_cls
class swelling_model(Group):
    """
    'swelling_model' child.
    """

    fluent_name = "swelling-model"

    child_names = \
        ['enabled', 'soc_ref', 'cell_type', 'axis_vec', 'normal_vec',
         'prism_axis_vec', 'prism_vec2', 'orientation_udf_name',
         'customize_swelling_strain', 'strain_udf_name']

    _child_classes = dict(
        enabled=enabled_cls,
        soc_ref=soc_ref_cls,
        cell_type=cell_type_cls,
        axis_vec=axis_vec_cls,
        normal_vec=normal_vec_cls,
        prism_axis_vec=prism_axis_vec_cls,
        prism_vec2=prism_vec2_cls,
        orientation_udf_name=orientation_udf_name_cls,
        customize_swelling_strain=customize_swelling_strain_cls,
        strain_udf_name=strain_udf_name_cls,
    )

