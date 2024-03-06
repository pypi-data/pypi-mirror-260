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
class slit_face_zone(Command):
    """
    Slit a two-sided wall into two connected wall zones.
    
    Parameters
    ----------
        zone_name : str
            Enter a zone name.
    
    """

    fluent_name = "slit-face-zone"

    argument_names = \
        ['zone_name']

    _child_classes = dict(
        zone_name=zone_name_cls,
    )

