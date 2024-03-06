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

from .nodes import nodes as nodes_cls
from .edges_1 import edges as edges_cls
from .faces_1 import faces as faces_cls
from .partitions import partitions as partitions_cls
from .overset_3 import overset as overset_cls
from .gap import gap as gap_cls
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['nodes', 'edges', 'faces', 'partitions', 'overset', 'gap']

    _child_classes = dict(
        nodes=nodes_cls,
        edges=edges_cls,
        faces=faces_cls,
        partitions=partitions_cls,
        overset=overset_cls,
        gap=gap_cls,
    )

