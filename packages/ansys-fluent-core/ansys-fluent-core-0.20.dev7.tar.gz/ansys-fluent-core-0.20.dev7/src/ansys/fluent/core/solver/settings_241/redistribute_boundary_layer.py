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

from .zone_name_1 import zone_name as zone_name_cls
from .growth_rate import growth_rate as growth_rate_cls
class redistribute_boundary_layer(Command):
    """
    Enforce growth rate in boundary layer.
    
    Parameters
    ----------
        zone_name : str
            Enter a zone name.
        growth_rate : real
            'growth_rate' child.
    
    """

    fluent_name = "redistribute-boundary-layer"

    argument_names = \
        ['zone_name', 'growth_rate']

    _child_classes = dict(
        zone_name=zone_name_cls,
        growth_rate=growth_rate_cls,
    )

