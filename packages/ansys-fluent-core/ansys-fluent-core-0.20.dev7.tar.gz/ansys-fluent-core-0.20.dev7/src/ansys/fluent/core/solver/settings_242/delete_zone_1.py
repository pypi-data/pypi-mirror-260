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

from .face_name_1 import face_name as face_name_cls
class delete_zone(Command):
    """
    Delete thread-real-pair object.
    
    Parameters
    ----------
        face_name : str
            Specify object name when deleting a thread-real-pair object.
    
    """

    fluent_name = "delete-zone"

    argument_names = \
        ['face_name']

    _child_classes = dict(
        face_name=face_name_cls,
    )

