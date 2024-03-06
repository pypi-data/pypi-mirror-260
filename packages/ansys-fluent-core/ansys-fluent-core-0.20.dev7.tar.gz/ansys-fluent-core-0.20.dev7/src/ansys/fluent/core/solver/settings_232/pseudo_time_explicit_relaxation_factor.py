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

from .local_dt_dualts_relax import local_dt_dualts_relax as local_dt_dualts_relax_cls
from .global_dt_pseudo_relax import global_dt_pseudo_relax as global_dt_pseudo_relax_cls
class pseudo_time_explicit_relaxation_factor(Group):
    """
    'pseudo_time_explicit_relaxation_factor' child.
    """

    fluent_name = "pseudo-time-explicit-relaxation-factor"

    child_names = \
        ['local_dt_dualts_relax', 'global_dt_pseudo_relax']

    _child_classes = dict(
        local_dt_dualts_relax=local_dt_dualts_relax_cls,
        global_dt_pseudo_relax=global_dt_pseudo_relax_cls,
    )

