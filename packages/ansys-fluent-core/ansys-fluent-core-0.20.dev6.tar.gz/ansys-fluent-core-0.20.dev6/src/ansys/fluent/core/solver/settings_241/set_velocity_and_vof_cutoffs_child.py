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

from .max_vel_mag import max_vel_mag as max_vel_mag_cls
from .vol_frac_cutoff import vol_frac_cutoff as vol_frac_cutoff_cls
class set_velocity_and_vof_cutoffs_child(Group):
    """
    'child_object_type' of set_velocity_and_vof_cutoffs.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['max_vel_mag', 'vol_frac_cutoff']

    _child_classes = dict(
        max_vel_mag=max_vel_mag_cls,
        vol_frac_cutoff=vol_frac_cutoff_cls,
    )

