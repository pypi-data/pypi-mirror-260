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

from .zone_name_9 import zone_name as zone_name_cls
class non_overlapping_zone_name(Command):
    """
    Get non-overlapping zone name from the associated interface zone.
    
    Parameters
    ----------
        zone_name : str
            Enter zone id/name.
    
    """

    fluent_name = "non-overlapping-zone-name"

    argument_names = \
        ['zone_name']

    _child_classes = dict(
        zone_name=zone_name_cls,
    )

