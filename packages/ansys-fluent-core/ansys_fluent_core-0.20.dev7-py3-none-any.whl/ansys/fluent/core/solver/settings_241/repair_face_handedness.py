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

from .repair_1 import repair as repair_cls
from .disable_repair import disable_repair as disable_repair_cls
class repair_face_handedness(Command):
    """
    Correct face handedness at left handed faces if possible.
    
    Parameters
    ----------
        repair : bool
            'repair' child.
        disable_repair : bool
            'disable_repair' child.
    
    """

    fluent_name = "repair-face-handedness"

    argument_names = \
        ['repair', 'disable_repair']

    _child_classes = dict(
        repair=repair_cls,
        disable_repair=disable_repair_cls,
    )

