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

from .slip_velocity_specification import slip_velocity_specification as slip_velocity_specification_cls
from .phase_velocity_ratio import phase_velocity_ratio as phase_velocity_ratio_cls
from .volume_fraction_1 import volume_fraction as volume_fraction_cls
from .granular_temperature_1 import granular_temperature as granular_temperature_cls
from .interfacial_area_concentration_1 import interfacial_area_concentration as interfacial_area_concentration_cls
class multiphase(Group):
    """
    Help not available.
    """

    fluent_name = "multiphase"

    child_names = \
        ['slip_velocity_specification', 'phase_velocity_ratio',
         'volume_fraction', 'granular_temperature',
         'interfacial_area_concentration']

    _child_classes = dict(
        slip_velocity_specification=slip_velocity_specification_cls,
        phase_velocity_ratio=phase_velocity_ratio_cls,
        volume_fraction=volume_fraction_cls,
        granular_temperature=granular_temperature_cls,
        interfacial_area_concentration=interfacial_area_concentration_cls,
    )

