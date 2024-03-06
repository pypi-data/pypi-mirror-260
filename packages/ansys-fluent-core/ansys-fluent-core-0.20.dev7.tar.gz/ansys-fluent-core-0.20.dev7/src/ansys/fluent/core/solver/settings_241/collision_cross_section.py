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

from .option_7 import option as option_cls
from .cross_section_multicomponent import cross_section_multicomponent as cross_section_multicomponent_cls
class collision_cross_section(Group):
    """
    'collision_cross_section' child.
    """

    fluent_name = "collision-cross-section"

    child_names = \
        ['option', 'cross_section_multicomponent']

    _child_classes = dict(
        option=option_cls,
        cross_section_multicomponent=cross_section_multicomponent_cls,
    )

