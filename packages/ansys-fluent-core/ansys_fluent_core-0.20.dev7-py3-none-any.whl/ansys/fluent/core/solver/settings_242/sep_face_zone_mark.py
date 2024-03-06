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
from .register_name import register_name as register_name_cls
from .move_faces import move_faces as move_faces_cls
class sep_face_zone_mark(Command):
    """
    Separate a face zone based on cell marking.
    
    Parameters
    ----------
        face_zone_name : str
            Enter a zone name.
        register_name : str
            'register_name' child.
        move_faces : bool
            'move_faces' child.
    
    """

    fluent_name = "sep-face-zone-mark"

    argument_names = \
        ['face_zone_name', 'register_name', 'move_faces']

    _child_classes = dict(
        face_zone_name=face_zone_name_cls,
        register_name=register_name_cls,
        move_faces=move_faces_cls,
    )

