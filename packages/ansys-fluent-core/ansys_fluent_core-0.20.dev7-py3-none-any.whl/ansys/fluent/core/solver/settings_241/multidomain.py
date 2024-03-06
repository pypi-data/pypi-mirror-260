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

from .conjugate_heat_transfer import conjugate_heat_transfer as conjugate_heat_transfer_cls
from .solve_1 import solve as solve_cls
class multidomain(Group):
    """
    Enter the multidomain architecture menu.
    """

    fluent_name = "multidomain"

    child_names = \
        ['conjugate_heat_transfer', 'solve']

    _child_classes = dict(
        conjugate_heat_transfer=conjugate_heat_transfer_cls,
        solve=solve_cls,
    )

