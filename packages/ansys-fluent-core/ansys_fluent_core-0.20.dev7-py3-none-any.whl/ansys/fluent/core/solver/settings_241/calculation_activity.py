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

from .execute_commands import execute_commands as execute_commands_cls
from .solution_animations import solution_animations as solution_animations_cls
from .case_modification_1 import case_modification as case_modification_cls
from .poor_mesh_numerics import poor_mesh_numerics as poor_mesh_numerics_cls
class calculation_activity(Group):
    """
    'calculation_activity' child.
    """

    fluent_name = "calculation-activity"

    child_names = \
        ['execute_commands', 'solution_animations', 'case_modification',
         'poor_mesh_numerics']

    _child_classes = dict(
        execute_commands=execute_commands_cls,
        solution_animations=solution_animations_cls,
        case_modification=case_modification_cls,
        poor_mesh_numerics=poor_mesh_numerics_cls,
    )

