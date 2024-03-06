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
from .poor_mesh_numerics import poor_mesh_numerics as poor_mesh_numerics_cls
from .enable_strategy import enable_strategy as enable_strategy_cls
from .copy_modification import copy_modification as copy_modification_cls
from .delete_modification import delete_modification as delete_modification_cls
from .enable_modification import enable_modification as enable_modification_cls
from .disable_modification import disable_modification as disable_modification_cls
from .import_modifications import import_modifications as import_modifications_cls
from .export_modifications import export_modifications as export_modifications_cls
from .continue_strategy_execution import continue_strategy_execution as continue_strategy_execution_cls
class calculation_activity(Group):
    """
    'calculation_activity' child.
    """

    fluent_name = "calculation-activity"

    child_names = \
        ['execute_commands', 'solution_animations', 'poor_mesh_numerics']

    command_names = \
        ['enable_strategy', 'copy_modification', 'delete_modification',
         'enable_modification', 'disable_modification',
         'import_modifications', 'export_modifications',
         'continue_strategy_execution']

    _child_classes = dict(
        execute_commands=execute_commands_cls,
        solution_animations=solution_animations_cls,
        poor_mesh_numerics=poor_mesh_numerics_cls,
        enable_strategy=enable_strategy_cls,
        copy_modification=copy_modification_cls,
        delete_modification=delete_modification_cls,
        enable_modification=enable_modification_cls,
        disable_modification=disable_modification_cls,
        import_modifications=import_modifications_cls,
        export_modifications=export_modifications_cls,
        continue_strategy_execution=continue_strategy_execution_cls,
    )

