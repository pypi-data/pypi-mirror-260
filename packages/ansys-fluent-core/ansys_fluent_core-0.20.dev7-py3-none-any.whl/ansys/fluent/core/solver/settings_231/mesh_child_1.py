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

from .name_1 import name as name_cls
from .options_5 import options as options_cls
from .edge_type import edge_type as edge_type_cls
from .shrink_factor import shrink_factor as shrink_factor_cls
from .surfaces_list import surfaces_list as surfaces_list_cls
from .coloring_1 import coloring as coloring_cls
from .display_state_name import display_state_name as display_state_name_cls
from .physics import physics as physics_cls
from .geometry_3 import geometry as geometry_cls
from .surfaces import surfaces as surfaces_cls
from .display_2 import display as display_cls
class mesh_child(Group):
    """
    'child_object_type' of mesh.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'options', 'edge_type', 'shrink_factor', 'surfaces_list',
         'coloring', 'display_state_name', 'physics', 'geometry', 'surfaces']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        options=options_cls,
        edge_type=edge_type_cls,
        shrink_factor=shrink_factor_cls,
        surfaces_list=surfaces_list_cls,
        coloring=coloring_cls,
        display_state_name=display_state_name_cls,
        physics=physics_cls,
        geometry=geometry_cls,
        surfaces=surfaces_cls,
        display=display_cls,
    )

