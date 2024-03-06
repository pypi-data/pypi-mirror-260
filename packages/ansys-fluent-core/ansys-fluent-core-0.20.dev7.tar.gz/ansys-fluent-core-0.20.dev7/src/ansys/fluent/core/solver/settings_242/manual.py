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

from .faces_2 import faces as faces_cls
from .edges_2 import edges as edges_cls
from .nodes_1 import nodes as nodes_cls
from .material_color import material_color as material_color_cls
class manual(Group):
    """
    'manual' child.
    """

    fluent_name = "manual"

    child_names = \
        ['faces', 'edges', 'nodes', 'material_color']

    _child_classes = dict(
        faces=faces_cls,
        edges=edges_cls,
        nodes=nodes_cls,
        material_color=material_color_cls,
    )

