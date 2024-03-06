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

from .thread_id import thread_id as thread_id_cls
from .growth_rate import growth_rate as growth_rate_cls
class redistribute_boundary_layer(Command):
    """
    Enforce growth rate in boundary layer.
    
    Parameters
    ----------
        thread_id : int
            'thread_id' child.
        growth_rate : real
            'growth_rate' child.
    
    """

    fluent_name = "redistribute-boundary-layer"

    argument_names = \
        ['thread_id', 'growth_rate']

    _child_classes = dict(
        thread_id=thread_id_cls,
        growth_rate=growth_rate_cls,
    )

