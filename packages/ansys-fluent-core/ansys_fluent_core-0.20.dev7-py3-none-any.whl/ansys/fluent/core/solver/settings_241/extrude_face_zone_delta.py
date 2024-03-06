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

from .face_zone import face_zone as face_zone_cls
from .distance_delta import distance_delta as distance_delta_cls
class extrude_face_zone_delta(Command):
    """
    Extrude a face thread a specified distance based on a list of deltas.
    
    Parameters
    ----------
        face_zone : str
            Enter a zone name.
        distance_delta : typing.List[real]
            'distance_delta' child.
    
    """

    fluent_name = "extrude-face-zone-delta"

    argument_names = \
        ['face_zone', 'distance_delta']

    _child_classes = dict(
        face_zone=face_zone_cls,
        distance_delta=distance_delta_cls,
    )

