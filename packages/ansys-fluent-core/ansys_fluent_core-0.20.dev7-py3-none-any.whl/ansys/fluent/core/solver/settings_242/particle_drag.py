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

from .option import option as option_cls
from .shape_factor import shape_factor as shape_factor_cls
from .cunningham_factor import cunningham_factor as cunningham_factor_cls
class particle_drag(Group):
    """
    'particle_drag' child.
    """

    fluent_name = "particle-drag"

    child_names = \
        ['option', 'shape_factor', 'cunningham_factor']

    _child_classes = dict(
        option=option_cls,
        shape_factor=shape_factor_cls,
        cunningham_factor=cunningham_factor_cls,
    )

