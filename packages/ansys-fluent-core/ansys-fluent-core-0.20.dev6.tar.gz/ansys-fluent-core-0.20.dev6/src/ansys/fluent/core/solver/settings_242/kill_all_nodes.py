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

from .delete_all_compute_nodes import delete_all_compute_nodes as delete_all_compute_nodes_cls
class kill_all_nodes(Command):
    """
    Delete all compute nodes from virtual machine.
    
    Parameters
    ----------
        delete_all_compute_nodes : bool
            'delete_all_compute_nodes' child.
    
    """

    fluent_name = "kill-all-nodes"

    argument_names = \
        ['delete_all_compute_nodes']

    _child_classes = dict(
        delete_all_compute_nodes=delete_all_compute_nodes_cls,
    )

