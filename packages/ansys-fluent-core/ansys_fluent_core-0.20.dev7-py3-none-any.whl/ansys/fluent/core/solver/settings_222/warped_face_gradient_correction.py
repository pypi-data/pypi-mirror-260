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

from .enable_3 import enable as enable_cls
from .turbulence_options import turbulence_options as turbulence_options_cls
class warped_face_gradient_correction(Group):
    """
    'warped_face_gradient_correction' child.
    """

    fluent_name = "warped-face-gradient-correction"

    child_names = \
        ['enable', 'turbulence_options']

    _child_classes = dict(
        enable=enable_cls,
        turbulence_options=turbulence_options_cls,
    )

