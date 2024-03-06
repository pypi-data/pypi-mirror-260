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

from .enable_15 import enable as enable_cls
from .mode_1 import mode as mode_cls
from .turbulence_options import turbulence_options as turbulence_options_cls
class warped_face_gradient_correction(Group):
    """
    Enter warped-face-gradient-correction menu.
    """

    fluent_name = "warped-face-gradient-correction"

    child_names = \
        ['enable', 'mode', 'turbulence_options']

    _child_classes = dict(
        enable=enable_cls,
        mode=mode_cls,
        turbulence_options=turbulence_options_cls,
    )

