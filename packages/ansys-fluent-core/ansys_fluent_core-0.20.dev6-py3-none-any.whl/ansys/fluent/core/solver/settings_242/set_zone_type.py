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

from .zone_list import zone_list as zone_list_cls
from .new_type import new_type as new_type_cls
class set_zone_type(Command):
    """
    Set a zone's type.
    
    Parameters
    ----------
        zone_list : typing.List[str]
            Enter zone name list.
        new_type : str
            Give new zone type.
    
    """

    fluent_name = "set-zone-type"

    argument_names = \
        ['zone_list', 'new_type']

    _child_classes = dict(
        zone_list=zone_list_cls,
        new_type=new_type_cls,
    )

