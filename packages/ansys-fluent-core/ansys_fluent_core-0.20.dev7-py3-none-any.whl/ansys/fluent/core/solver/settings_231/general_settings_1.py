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

from .iter_count_1 import iter_count as iter_count_cls
from .explicit_urf import explicit_urf as explicit_urf_cls
from .reference_frame_2 import reference_frame as reference_frame_cls
from .initial_pressure import initial_pressure as initial_pressure_cls
from .external_aero import external_aero as external_aero_cls
from .const_velocity import const_velocity as const_velocity_cls
class general_settings(Group):
    """
    Enter the general settings menu.
    """

    fluent_name = "general-settings"

    child_names = \
        ['iter_count', 'explicit_urf', 'reference_frame', 'initial_pressure',
         'external_aero', 'const_velocity']

    _child_classes = dict(
        iter_count=iter_count_cls,
        explicit_urf=explicit_urf_cls,
        reference_frame=reference_frame_cls,
        initial_pressure=initial_pressure_cls,
        external_aero=external_aero_cls,
        const_velocity=const_velocity_cls,
    )

