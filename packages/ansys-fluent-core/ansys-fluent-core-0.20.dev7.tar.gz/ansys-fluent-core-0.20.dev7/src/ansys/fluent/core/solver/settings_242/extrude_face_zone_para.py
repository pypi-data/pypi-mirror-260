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
from .normal_distance import normal_distance as normal_distance_cls
from .parametric_coordinates import parametric_coordinates as parametric_coordinates_cls
class extrude_face_zone_para(Command):
    """
    Extrude a face thread a specified distance based on a distance and a list of parametric locations between 0 and 1 (eg. 0 0.2 0.4 0.8 1.0).
    
    Parameters
    ----------
        face_zone : str
            Enter a zone name.
        normal_distance : real
            'normal_distance' child.
        parametric_coordinates : typing.List[real]
            'parametric_coordinates' child.
    
    """

    fluent_name = "extrude-face-zone-para"

    argument_names = \
        ['face_zone', 'normal_distance', 'parametric_coordinates']

    _child_classes = dict(
        face_zone=face_zone_cls,
        normal_distance=normal_distance_cls,
        parametric_coordinates=parametric_coordinates_cls,
    )

