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

from .schost import schost as schost_cls
from .scport import scport as scport_cls
from .scname import scname as scname_cls
class connect_parallel(Command):
    """
    System coupling connection status.
    
    Parameters
    ----------
        schost : str
            Sc solver host input.
        scport : int
            Sc solver port input.
        scname : str
            Sc solver name input.
    
    """

    fluent_name = "connect-parallel"

    argument_names = \
        ['schost', 'scport', 'scname']

    _child_classes = dict(
        schost=schost_cls,
        scport=scport_cls,
        scname=scname_cls,
    )

