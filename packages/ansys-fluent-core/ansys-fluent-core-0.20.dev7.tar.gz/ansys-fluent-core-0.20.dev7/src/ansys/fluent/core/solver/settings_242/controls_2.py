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

from .solution_based_initialization import solution_based_initialization as solution_based_initialization_cls
from .auto_adjust import auto_adjust as auto_adjust_cls
from .advancement import advancement as advancement_cls
from .under_relaxation_3 import under_relaxation as under_relaxation_cls
from .amg_1 import amg as amg_cls
from .stabilization_1 import stabilization as stabilization_cls
from .default_4 import default as default_cls
class controls(Group):
    """
    Enter the adjoint controls menu.
    """

    fluent_name = "controls"

    child_names = \
        ['solution_based_initialization', 'auto_adjust', 'advancement',
         'under_relaxation', 'amg', 'stabilization']

    command_names = \
        ['default']

    _child_classes = dict(
        solution_based_initialization=solution_based_initialization_cls,
        auto_adjust=auto_adjust_cls,
        advancement=advancement_cls,
        under_relaxation=under_relaxation_cls,
        amg=amg_cls,
        stabilization=stabilization_cls,
        default=default_cls,
    )

