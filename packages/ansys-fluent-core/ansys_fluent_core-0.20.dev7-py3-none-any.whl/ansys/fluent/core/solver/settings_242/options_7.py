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

from .relaxation_factor import relaxation_factor as relaxation_factor_cls
from .select_variables import select_variables as select_variables_cls
from .type_7 import type as type_cls
class options(Group):
    """
    High Order Term Relaxation Options.
    """

    fluent_name = "options"

    child_names = \
        ['relaxation_factor', 'select_variables', 'type']

    _child_classes = dict(
        relaxation_factor=relaxation_factor_cls,
        select_variables=select_variables_cls,
        type=type_cls,
    )

