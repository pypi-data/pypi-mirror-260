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
from .growth_ratio_refinement import growth_ratio_refinement as growth_ratio_refinement_cls
class type(Group):
    """
    'type' child.
    """

    fluent_name = "type"

    child_names = \
        ['option', 'growth_ratio_refinement']

    _child_classes = dict(
        option=option_cls,
        growth_ratio_refinement=growth_ratio_refinement_cls,
    )

