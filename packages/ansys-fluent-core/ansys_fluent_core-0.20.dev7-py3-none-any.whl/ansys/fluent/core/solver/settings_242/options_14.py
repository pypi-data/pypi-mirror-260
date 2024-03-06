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

from .node_values_1 import node_values as node_values_cls
class options(Group):
    """
    Check the control options.
    """

    fluent_name = "options"

    child_names = \
        ['node_values']

    _child_classes = dict(
        node_values=node_values_cls,
    )

