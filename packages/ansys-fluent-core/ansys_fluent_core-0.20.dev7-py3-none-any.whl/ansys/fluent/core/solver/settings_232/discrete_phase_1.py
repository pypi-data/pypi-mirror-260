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

from .histogram import histogram as histogram_cls
from .sample_trajectories import sample_trajectories as sample_trajectories_cls
from .summary import summary as summary_cls
from .extended_summary import extended_summary as extended_summary_cls
from .zone_summaries_per_injection import zone_summaries_per_injection as zone_summaries_per_injection_cls
class discrete_phase(Group):
    """
    'discrete_phase' child.
    """

    fluent_name = "discrete-phase"

    child_names = \
        ['histogram', 'sample_trajectories']

    command_names = \
        ['summary', 'extended_summary', 'zone_summaries_per_injection']

    _child_classes = dict(
        histogram=histogram_cls,
        sample_trajectories=sample_trajectories_cls,
        summary=summary_cls,
        extended_summary=extended_summary_cls,
        zone_summaries_per_injection=zone_summaries_per_injection_cls,
    )

