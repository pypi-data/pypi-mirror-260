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

from .les_zone_1 import les_zone as les_zone_cls
from .udf_zmotion_name import udf_zmotion_name as udf_zmotion_name_cls
from .axis_origin_1 import axis_origin as axis_origin_cls
from .axis_direction_1 import axis_direction as axis_direction_cls
from .omega import omega as omega_cls
from .relative_to_thread import relative_to_thread as relative_to_thread_cls
from .motion_spec import motion_spec as motion_spec_cls
from .cylindrical_fixed_var import cylindrical_fixed_var as cylindrical_fixed_var_cls
class disabled(Group):
    """
    Help not available.
    """

    fluent_name = "disabled"

    child_names = \
        ['les_zone', 'udf_zmotion_name', 'axis_origin', 'axis_direction',
         'omega', 'relative_to_thread', 'motion_spec',
         'cylindrical_fixed_var']

    _child_classes = dict(
        les_zone=les_zone_cls,
        udf_zmotion_name=udf_zmotion_name_cls,
        axis_origin=axis_origin_cls,
        axis_direction=axis_direction_cls,
        omega=omega_cls,
        relative_to_thread=relative_to_thread_cls,
        motion_spec=motion_spec_cls,
        cylindrical_fixed_var=cylindrical_fixed_var_cls,
    )

