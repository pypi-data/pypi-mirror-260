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
from .abbrev import abbrev as abbrev_cls
from .exclude import exclude as exclude_cls
class rename_to_default(Command):
    """
    Rename zone to default name.
    
    Parameters
    ----------
        zone_name : typing.List[str]
            Enter zone name list.
        abbrev : bool
            Select to provide abbreviate types.
        exclude : bool
            Select to exclude custom names.
    
    """

    fluent_name = "rename-to-default"

    argument_names = \
        ['zone_name', 'abbrev', 'exclude']

    _child_classes = dict(
        zone_name=zone_name_cls,
        abbrev=abbrev_cls,
        exclude=exclude_cls,
    )

