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

from .compute_node import compute_node as compute_node_cls
from .invalidate_case import invalidate_case as invalidate_case_cls
class kill_node(Command):
    """
    'kill_node' command.
    
    Parameters
    ----------
        compute_node : int
            'compute_node' child.
        invalidate_case : bool
            'invalidate_case' child.
    
    """

    fluent_name = "kill-node"

    argument_names = \
        ['compute_node', 'invalidate_case']

    _child_classes = dict(
        compute_node=compute_node_cls,
        invalidate_case=invalidate_case_cls,
    )

