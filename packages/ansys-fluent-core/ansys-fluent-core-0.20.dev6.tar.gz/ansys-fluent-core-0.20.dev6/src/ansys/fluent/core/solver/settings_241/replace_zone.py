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

from .file_name_1 import file_name as file_name_cls
from .zone_1_name import zone_1_name as zone_1_name_cls
from .zone_2_name import zone_2_name as zone_2_name_cls
from .interpolate import interpolate as interpolate_cls
class replace_zone(Command):
    """
    Replace a cell zone.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        zone_1_name : str
            Enter a zone name.
        zone_2_name : str
            'zone_2_name' child.
        interpolate : bool
            'interpolate' child.
    
    """

    fluent_name = "replace-zone"

    argument_names = \
        ['file_name', 'zone_1_name', 'zone_2_name', 'interpolate']

    _child_classes = dict(
        file_name=file_name_cls,
        zone_1_name=zone_1_name_cls,
        zone_2_name=zone_2_name_cls,
        interpolate=interpolate_cls,
    )

