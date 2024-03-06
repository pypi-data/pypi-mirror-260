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

from .name_2 import name as name_cls
from .zone_list_1 import zone_list_1 as zone_list_1_cls
from .zone_list_2 import zone_list_2 as zone_list_2_cls
class create_manually(Command):
    """
    Create one-to-one interfaces between two groups of boundary zones even if they do not currently overlap.
    
    Parameters
    ----------
        name : str
            Enter a prefix for mesh interface names.
        zone_list_1 : typing.List[str]
            Enter the boundary zones belonging to the first group.
        zone_list_2 : typing.List[str]
            Enter the boundary zones belonging to the second group.
    
    """

    fluent_name = "create-manually"

    argument_names = \
        ['name', 'zone_list_1', 'zone_list_2']

    _child_classes = dict(
        name=name_cls,
        zone_list_1=zone_list_1_cls,
        zone_list_2=zone_list_2_cls,
    )

