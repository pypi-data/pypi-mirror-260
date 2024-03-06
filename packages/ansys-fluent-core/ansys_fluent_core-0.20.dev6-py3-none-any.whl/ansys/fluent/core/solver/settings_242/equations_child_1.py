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

from .monitor import monitor as monitor_cls
from .normalization_factor import normalization_factor as normalization_factor_cls
from .check_convergence import check_convergence as check_convergence_cls
from .absolute_criteria import absolute_criteria as absolute_criteria_cls
from .relative_criteria import relative_criteria as relative_criteria_cls
class equations_child(Group):
    """
    'child_object_type' of equations.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['monitor', 'normalization_factor', 'check_convergence',
         'absolute_criteria', 'relative_criteria']

    _child_classes = dict(
        monitor=monitor_cls,
        normalization_factor=normalization_factor_cls,
        check_convergence=check_convergence_cls,
        absolute_criteria=absolute_criteria_cls,
        relative_criteria=relative_criteria_cls,
    )

