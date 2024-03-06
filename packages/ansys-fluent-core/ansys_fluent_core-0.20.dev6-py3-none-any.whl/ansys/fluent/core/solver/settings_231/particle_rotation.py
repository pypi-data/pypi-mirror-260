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

from .enable import enable as enable_cls
from .drag_law import drag_law as drag_law_cls
from .lift_law import lift_law as lift_law_cls
class particle_rotation(Group):
    """
    'particle_rotation' child.
    """

    fluent_name = "particle-rotation"

    child_names = \
        ['enable', 'drag_law', 'lift_law']

    _child_classes = dict(
        enable=enable_cls,
        drag_law=drag_law_cls,
        lift_law=lift_law_cls,
    )

