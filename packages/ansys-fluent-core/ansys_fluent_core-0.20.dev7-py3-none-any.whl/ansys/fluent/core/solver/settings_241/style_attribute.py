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

from .style import style as style_cls
from .line_width import line_width as line_width_cls
from .arrow_space import arrow_space as arrow_space_cls
from .arrow_scale import arrow_scale as arrow_scale_cls
from .marker_size_1 import marker_size as marker_size_cls
from .sphere_size import sphere_size as sphere_size_cls
from .sphere_lod import sphere_lod as sphere_lod_cls
from .radius import radius as radius_cls
from .ribbon import ribbon as ribbon_cls
class style_attribute(Group):
    """
    'style_attribute' child.
    """

    fluent_name = "style-attribute"

    child_names = \
        ['style', 'line_width', 'arrow_space', 'arrow_scale', 'marker_size',
         'sphere_size', 'sphere_lod', 'radius', 'ribbon']

    _child_classes = dict(
        style=style_cls,
        line_width=line_width_cls,
        arrow_space=arrow_space_cls,
        arrow_scale=arrow_scale_cls,
        marker_size=marker_size_cls,
        sphere_size=sphere_size_cls,
        sphere_lod=sphere_lod_cls,
        radius=radius_cls,
        ribbon=ribbon_cls,
    )

