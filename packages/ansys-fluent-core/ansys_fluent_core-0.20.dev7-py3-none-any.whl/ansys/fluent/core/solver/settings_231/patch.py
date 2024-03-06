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

from .vof_smooth_options import vof_smooth_options as vof_smooth_options_cls
from .calculate_patch import calculate_patch as calculate_patch_cls
class patch(Group):
    """
    'patch' child.
    """

    fluent_name = "patch"

    child_names = \
        ['vof_smooth_options']

    command_names = \
        ['calculate_patch']

    _child_classes = dict(
        vof_smooth_options=vof_smooth_options_cls,
        calculate_patch=calculate_patch_cls,
    )

