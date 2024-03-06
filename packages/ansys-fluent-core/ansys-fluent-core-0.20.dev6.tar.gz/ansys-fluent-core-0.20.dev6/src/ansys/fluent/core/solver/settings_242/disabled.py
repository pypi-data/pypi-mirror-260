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

from .udf_zmotion_name import udf_zmotion_name as udf_zmotion_name_cls
from .axis_direction_1 import axis_direction as axis_direction_cls
from .axis_origin_1 import axis_origin as axis_origin_cls
from .cursys import cursys as cursys_cls
from .solid_omega import solid_omega as solid_omega_cls
from .solid_relative_to_thread import solid_relative_to_thread as solid_relative_to_thread_cls
from .enable_13 import enable as enable_cls
from .solid_motion_axis_direction import solid_motion_axis_direction as solid_motion_axis_direction_cls
from .solid_motion_axis_origin import solid_motion_axis_origin as solid_motion_axis_origin_cls
from .solid_motion_velocity import solid_motion_velocity as solid_motion_velocity_cls
from .solid_motion_zone_motion_function import solid_motion_zone_motion_function as solid_motion_zone_motion_function_cls
from .omega_1 import omega as omega_cls
from .relative_to_thread import relative_to_thread as relative_to_thread_cls
from .motion_spec import motion_spec as motion_spec_cls
class disabled(Group):
    """
    Help not available.
    """

    fluent_name = "disabled"

    child_names = \
        ['udf_zmotion_name', 'axis_direction', 'axis_origin', 'cursys',
         'solid_omega', 'solid_relative_to_thread', 'enable',
         'solid_motion_axis_direction', 'solid_motion_axis_origin',
         'solid_motion_velocity', 'solid_motion_zone_motion_function',
         'omega', 'relative_to_thread', 'motion_spec']

    _child_classes = dict(
        udf_zmotion_name=udf_zmotion_name_cls,
        axis_direction=axis_direction_cls,
        axis_origin=axis_origin_cls,
        cursys=cursys_cls,
        solid_omega=solid_omega_cls,
        solid_relative_to_thread=solid_relative_to_thread_cls,
        enable=enable_cls,
        solid_motion_axis_direction=solid_motion_axis_direction_cls,
        solid_motion_axis_origin=solid_motion_axis_origin_cls,
        solid_motion_velocity=solid_motion_velocity_cls,
        solid_motion_zone_motion_function=solid_motion_zone_motion_function_cls,
        omega=omega_cls,
        relative_to_thread=relative_to_thread_cls,
        motion_spec=motion_spec_cls,
    )

