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

from .viscous_scale import viscous_scale as viscous_scale_cls
from .gravity_scale import gravity_scale as gravity_scale_cls
from .surface_tension_scale import surface_tension_scale as surface_tension_scale_cls
from .acoustic_scale import acoustic_scale as acoustic_scale_cls
class time_scale_options(Group):
    """
    Set physics based time scale options.
    """

    fluent_name = "time-scale-options"

    child_names = \
        ['viscous_scale', 'gravity_scale', 'surface_tension_scale',
         'acoustic_scale']

    _child_classes = dict(
        viscous_scale=viscous_scale_cls,
        gravity_scale=gravity_scale_cls,
        surface_tension_scale=surface_tension_scale_cls,
        acoustic_scale=acoustic_scale_cls,
    )

