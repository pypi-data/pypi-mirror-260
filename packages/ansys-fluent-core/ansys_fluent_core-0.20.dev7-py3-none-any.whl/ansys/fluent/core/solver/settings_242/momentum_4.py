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

from .reference_frame_3 import reference_frame as reference_frame_cls
from .mass_flow_specification import mass_flow_specification as mass_flow_specification_cls
from .mass_flow_rate_1 import mass_flow_rate as mass_flow_rate_cls
from .exit_corrected_mass_flow_rate import exit_corrected_mass_flow_rate as exit_corrected_mass_flow_rate_cls
from .mass_flux import mass_flux as mass_flux_cls
from .average_mass_flux import average_mass_flux as average_mass_flux_cls
from .ecmf_reference_temperature import ecmf_reference_temperature as ecmf_reference_temperature_cls
from .ecmf_reference_gauge_pressure import ecmf_reference_gauge_pressure as ecmf_reference_gauge_pressure_cls
class momentum(Group):
    """
    Help not available.
    """

    fluent_name = "momentum"

    child_names = \
        ['reference_frame', 'mass_flow_specification', 'mass_flow_rate',
         'exit_corrected_mass_flow_rate', 'mass_flux', 'average_mass_flux',
         'ecmf_reference_temperature', 'ecmf_reference_gauge_pressure']

    _child_classes = dict(
        reference_frame=reference_frame_cls,
        mass_flow_specification=mass_flow_specification_cls,
        mass_flow_rate=mass_flow_rate_cls,
        exit_corrected_mass_flow_rate=exit_corrected_mass_flow_rate_cls,
        mass_flux=mass_flux_cls,
        average_mass_flux=average_mass_flux_cls,
        ecmf_reference_temperature=ecmf_reference_temperature_cls,
        ecmf_reference_gauge_pressure=ecmf_reference_gauge_pressure_cls,
    )

