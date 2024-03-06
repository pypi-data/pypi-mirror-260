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

from .patch_reconstructed_interface import patch_reconstructed_interface as patch_reconstructed_interface_cls
from .use_volumetric_smoothing import use_volumetric_smoothing as use_volumetric_smoothing_cls
from .smoothing_relaxation_factor import smoothing_relaxation_factor as smoothing_relaxation_factor_cls
from .execute_smoothing import execute_smoothing as execute_smoothing_cls
class vof_smooth_options(Group):
    """
    'vof_smooth_options' child.
    """

    fluent_name = "vof-smooth-options"

    child_names = \
        ['patch_reconstructed_interface', 'use_volumetric_smoothing',
         'smoothing_relaxation_factor']

    command_names = \
        ['execute_smoothing']

    _child_classes = dict(
        patch_reconstructed_interface=patch_reconstructed_interface_cls,
        use_volumetric_smoothing=use_volumetric_smoothing_cls,
        smoothing_relaxation_factor=smoothing_relaxation_factor_cls,
        execute_smoothing=execute_smoothing_cls,
    )

