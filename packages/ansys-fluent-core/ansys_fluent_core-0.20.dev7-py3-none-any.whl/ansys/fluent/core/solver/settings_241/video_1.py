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

from .fps import fps as fps_cls
from .format_2 import format as format_cls
from .quality_2 import quality as quality_cls
from .name_4 import name as name_cls
from .use_original_resolution import use_original_resolution as use_original_resolution_cls
from .scale_6 import scale as scale_cls
from .set_standard_resolution import set_standard_resolution as set_standard_resolution_cls
from .width_2 import width as width_cls
from .height_2 import height as height_cls
from .advance_quality import advance_quality as advance_quality_cls
class video(Group):
    """
    'video' child.
    """

    fluent_name = "video"

    child_names = \
        ['fps', 'format', 'quality', 'name', 'use_original_resolution',
         'scale', 'set_standard_resolution', 'width', 'height',
         'advance_quality']

    _child_classes = dict(
        fps=fps_cls,
        format=format_cls,
        quality=quality_cls,
        name=name_cls,
        use_original_resolution=use_original_resolution_cls,
        scale=scale_cls,
        set_standard_resolution=set_standard_resolution_cls,
        width=width_cls,
        height=height_cls,
        advance_quality=advance_quality_cls,
    )

