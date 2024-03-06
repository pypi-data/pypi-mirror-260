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

from .face_pressure_options import face_pressure_options as face_pressure_options_cls
class face_pressure_controls(Group):
    """
    Enter the face pressure expert controls menu.
    """

    fluent_name = "face-pressure-controls"

    child_names = \
        ['face_pressure_options']

    _child_classes = dict(
        face_pressure_options=face_pressure_options_cls,
    )

