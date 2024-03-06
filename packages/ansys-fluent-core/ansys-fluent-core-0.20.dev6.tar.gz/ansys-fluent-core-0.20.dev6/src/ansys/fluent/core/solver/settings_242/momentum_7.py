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

from .gauge_pressure import gauge_pressure as gauge_pressure_cls
from .m_1 import m as m_cls
from .non_equil_boundary import non_equil_boundary as non_equil_boundary_cls
from .coordinate_system import coordinate_system as coordinate_system_cls
from .flow_direction import flow_direction as flow_direction_cls
from .axis_direction_2 import axis_direction as axis_direction_cls
from .axis_origin_2 import axis_origin as axis_origin_cls
class momentum(Group):
    """
    Help not available.
    """

    fluent_name = "momentum"

    child_names = \
        ['gauge_pressure', 'm', 'non_equil_boundary', 'coordinate_system',
         'flow_direction', 'axis_direction', 'axis_origin']

    _child_classes = dict(
        gauge_pressure=gauge_pressure_cls,
        m=m_cls,
        non_equil_boundary=non_equil_boundary_cls,
        coordinate_system=coordinate_system_cls,
        flow_direction=flow_direction_cls,
        axis_direction=axis_direction_cls,
        axis_origin=axis_origin_cls,
    )

