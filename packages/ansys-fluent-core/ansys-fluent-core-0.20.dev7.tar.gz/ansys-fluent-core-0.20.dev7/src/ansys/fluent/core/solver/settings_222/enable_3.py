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

from .enable_fast_mode import enable_fast_mode as enable_fast_mode_cls
from .enable_memory_saving_mode import enable_memory_saving_mode as enable_memory_saving_mode_cls
from .disable_warped_face_gradient_correction import disable_warped_face_gradient_correction as disable_warped_face_gradient_correction_cls
class enable(Group):
    """
    'enable' child.
    """

    fluent_name = "enable?"

    child_names = \
        ['enable_fast_mode', 'enable_memory_saving_mode']

    command_names = \
        ['disable_warped_face_gradient_correction']

    _child_classes = dict(
        enable_fast_mode=enable_fast_mode_cls,
        enable_memory_saving_mode=enable_memory_saving_mode_cls,
        disable_warped_face_gradient_correction=disable_warped_face_gradient_correction_cls,
    )

