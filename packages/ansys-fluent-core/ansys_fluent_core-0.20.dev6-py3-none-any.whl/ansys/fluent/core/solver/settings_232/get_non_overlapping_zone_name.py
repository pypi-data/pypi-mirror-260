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

from .zone_name_2 import zone_name as zone_name_cls
class get_non_overlapping_zone_name(Query):
    """
    Get non-overlapping zone name from the associated interface zone.
    
    Parameters
    ----------
        zone_name : str
            Enter zone name.
    
    """

    fluent_name = "get-non-overlapping-zone-name"

    argument_names = \
        ['zone_name']

    _child_classes = dict(
        zone_name=zone_name_cls,
    )

