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

from .location import location as location_cls
from .matrix import matrix as matrix_cls
from .cone_settings import cone_settings as cone_settings_cls
from .velocity import velocity as velocity_cls
from .angular_velocity import angular_velocity as angular_velocity_cls
from .flow_rate_1 import flow_rate as flow_rate_cls
from .times import times as times_cls
from .diameter_1 import diameter as diameter_cls
from .temperature import temperature as temperature_cls
from .temperature_2 import temperature_2 as temperature_2_cls
class initial_props(Group):
    """
    'initial_props' child.
    """

    fluent_name = "initial-props"

    child_names = \
        ['location', 'matrix', 'cone_settings', 'velocity',
         'angular_velocity', 'flow_rate', 'times', 'diameter', 'temperature',
         'temperature_2']

    _child_classes = dict(
        location=location_cls,
        matrix=matrix_cls,
        cone_settings=cone_settings_cls,
        velocity=velocity_cls,
        angular_velocity=angular_velocity_cls,
        flow_rate=flow_rate_cls,
        times=times_cls,
        diameter=diameter_cls,
        temperature=temperature_cls,
        temperature_2=temperature_2_cls,
    )

