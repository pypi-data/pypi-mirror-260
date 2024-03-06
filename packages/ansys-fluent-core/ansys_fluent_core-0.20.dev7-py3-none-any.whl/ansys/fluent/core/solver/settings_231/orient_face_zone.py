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

from .face_zone_id import face_zone_id as face_zone_id_cls
class orient_face_zone(Command):
    """
    Orient the face zone.
    
    Parameters
    ----------
        face_zone_id : int
            'face_zone_id' child.
    
    """

    fluent_name = "orient-face-zone"

    argument_names = \
        ['face_zone_id']

    _child_classes = dict(
        face_zone_id=face_zone_id_cls,
    )

