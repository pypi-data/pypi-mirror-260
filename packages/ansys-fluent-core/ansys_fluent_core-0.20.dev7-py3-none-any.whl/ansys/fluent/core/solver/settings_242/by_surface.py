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

from .use_inherent_material_color_1 import use_inherent_material_color as use_inherent_material_color_cls
from .reset_2 import reset as reset_cls
from .list_surfaces_by_color import list_surfaces_by_color as list_surfaces_by_color_cls
from .list_surfaces_by_material import list_surfaces_by_material as list_surfaces_by_material_cls
from .surfaces_8 import surfaces as surfaces_cls
class by_surface(Group):
    """
    'by_surface' child.
    """

    fluent_name = "by-surface"

    child_names = \
        ['use_inherent_material_color']

    command_names = \
        ['reset', 'list_surfaces_by_color', 'list_surfaces_by_material',
         'surfaces']

    _child_classes = dict(
        use_inherent_material_color=use_inherent_material_color_cls,
        reset=reset_cls,
        list_surfaces_by_color=list_surfaces_by_color_cls,
        list_surfaces_by_material=list_surfaces_by_material_cls,
        surfaces=surfaces_cls,
    )

