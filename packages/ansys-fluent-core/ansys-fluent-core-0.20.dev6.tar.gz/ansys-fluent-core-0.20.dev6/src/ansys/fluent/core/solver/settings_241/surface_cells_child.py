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

from .name import name as name_cls
from .surface_3 import surface as surface_cls
from .display_3 import display as display_cls
class surface_cells_child(Group):
    """
    'child_object_type' of surface_cells.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'surface']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        surface=surface_cls,
        display=display_cls,
    )

