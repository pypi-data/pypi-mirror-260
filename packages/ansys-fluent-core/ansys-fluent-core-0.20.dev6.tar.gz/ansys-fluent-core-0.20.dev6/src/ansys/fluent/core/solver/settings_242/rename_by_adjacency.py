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

from .zone_name_8 import zone_name as zone_name_cls
from .abbreviate_types import abbreviate_types as abbreviate_types_cls
from .exclude import exclude as exclude_cls
class rename_by_adjacency(Command):
    """
    Rename zone to adjacent zones.
    
    Parameters
    ----------
        zone_name : typing.List[str]
            Enter zone name list.
        abbreviate_types : bool
            Select to provide abbreviate types.
        exclude : bool
            Select to exclude custom names.
    
    """

    fluent_name = "rename-by-adjacency"

    argument_names = \
        ['zone_name', 'abbreviate_types', 'exclude']

    _child_classes = dict(
        zone_name=zone_name_cls,
        abbreviate_types=abbreviate_types_cls,
        exclude=exclude_cls,
    )

