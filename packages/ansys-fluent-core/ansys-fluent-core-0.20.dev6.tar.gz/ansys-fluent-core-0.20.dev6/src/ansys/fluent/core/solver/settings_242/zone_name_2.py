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
from .new_name import new_name as new_name_cls
class zone_name(Command):
    """
    Give a zone a new name.
    
    Parameters
    ----------
        zone_name : str
            Enter a zone name.
        new_name : str
            'new_name' child.
    
    """

    fluent_name = "zone-name"

    argument_names = \
        ['zone_name', 'new_name']

    _child_classes = dict(
        zone_name=zone_name_cls,
        new_name=new_name_cls,
    )

