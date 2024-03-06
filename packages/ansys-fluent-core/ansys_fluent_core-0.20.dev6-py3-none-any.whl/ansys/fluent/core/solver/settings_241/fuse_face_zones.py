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

from .zone_names import zone_names as zone_names_cls
from .zone_name import zone_name as zone_name_cls
class fuse_face_zones(Command):
    """
    Attempt to fuse zones by removing duplicate faces and nodes.
    
    Parameters
    ----------
        zone_names : typing.List[str]
            Merge duplicate faces and nodes of zones in list.
        zone_name : str
            'zone_name' child.
    
    """

    fluent_name = "fuse-face-zones"

    argument_names = \
        ['zone_names', 'zone_name']

    _child_classes = dict(
        zone_names=zone_names_cls,
        zone_name=zone_name_cls,
    )

