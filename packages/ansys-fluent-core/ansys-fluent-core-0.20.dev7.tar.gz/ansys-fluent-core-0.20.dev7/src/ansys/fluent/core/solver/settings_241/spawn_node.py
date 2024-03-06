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

from .hostname import hostname as hostname_cls
from .username import username as username_cls
class spawn_node(Command):
    """
    Spawn a compute node process on a specified machine.
    
    Parameters
    ----------
        hostname : str
            'hostname' child.
        username : str
            'username' child.
    
    """

    fluent_name = "spawn-node"

    argument_names = \
        ['hostname', 'username']

    _child_classes = dict(
        hostname=hostname_cls,
        username=username_cls,
    )

