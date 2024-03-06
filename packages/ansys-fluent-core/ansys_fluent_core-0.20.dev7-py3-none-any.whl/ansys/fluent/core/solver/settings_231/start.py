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

from .address import address as address_cls
from .port import port as port_cls
class start(Command):
    """
    'start' command.
    
    Parameters
    ----------
        address : str
            'address' child.
        port : int
            'port' child.
    
    """

    fluent_name = "start"

    argument_names = \
        ['address', 'port']

    _child_classes = dict(
        address=address_cls,
        port=port_cls,
    )

