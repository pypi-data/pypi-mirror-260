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

from .quality_1 import quality as quality_cls
from .denoiser import denoiser as denoiser_cls
from .thread_count import thread_count as thread_count_cls
from .max_rendering_timeout import max_rendering_timeout as max_rendering_timeout_cls
class rendering(Group):
    """
    Enter the menu for rendering options.
    """

    fluent_name = "rendering"

    child_names = \
        ['quality', 'denoiser', 'thread_count', 'max_rendering_timeout']

    _child_classes = dict(
        quality=quality_cls,
        denoiser=denoiser_cls,
        thread_count=thread_count_cls,
        max_rendering_timeout=max_rendering_timeout_cls,
    )

