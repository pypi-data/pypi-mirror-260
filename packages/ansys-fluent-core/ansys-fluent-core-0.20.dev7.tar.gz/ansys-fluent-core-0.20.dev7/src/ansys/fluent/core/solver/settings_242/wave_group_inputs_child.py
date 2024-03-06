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

from .theory import theory as theory_cls
from .wave_ht import wave_ht as wave_ht_cls
from .wave_len import wave_len as wave_len_cls
from .phase_diff import phase_diff as phase_diff_cls
from .heading_angle import heading_angle as heading_angle_cls
class wave_group_inputs_child(Group):
    """
    'child_object_type' of wave_group_inputs.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['theory', 'wave_ht', 'wave_len', 'phase_diff', 'heading_angle']

    _child_classes = dict(
        theory=theory_cls,
        wave_ht=wave_ht_cls,
        wave_len=wave_len_cls,
        phase_diff=phase_diff_cls,
        heading_angle=heading_angle_cls,
    )

