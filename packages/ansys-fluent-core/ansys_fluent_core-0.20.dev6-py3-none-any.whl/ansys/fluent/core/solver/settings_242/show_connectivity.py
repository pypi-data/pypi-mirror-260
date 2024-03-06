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
class show_connectivity(Command):
    """
    Show machine connectivity.
    
    Parameters
    ----------
        compute_node : int
            'compute_node' child.
    
    """

    fluent_name = "show-connectivity"

    argument_names = \
        ['compute_node']

    _child_classes = dict(
        compute_node=compute_node_cls,
    )

