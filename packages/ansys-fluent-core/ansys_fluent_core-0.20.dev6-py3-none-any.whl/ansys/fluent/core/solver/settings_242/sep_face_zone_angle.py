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

from .face_zone_name import face_zone_name as face_zone_name_cls
from .angle import angle as angle_cls
from .move_faces import move_faces as move_faces_cls
class sep_face_zone_angle(Command):
    """
    Separate a face zone based on significant angle.
    
    Parameters
    ----------
        face_zone_name : str
            Enter a zone name.
        angle : real
            'angle' child.
        move_faces : bool
            'move_faces' child.
    
    """

    fluent_name = "sep-face-zone-angle"

    argument_names = \
        ['face_zone_name', 'angle', 'move_faces']

    _child_classes = dict(
        face_zone_name=face_zone_name_cls,
        angle=angle_cls,
        move_faces=move_faces_cls,
    )

