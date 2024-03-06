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

from .general_nrbc import general_nrbc as general_nrbc_cls
from .turbo_sepcific_nrbc import turbo_sepcific_nrbc as turbo_sepcific_nrbc_cls
class non_reflecting_bc(Group):
    """
    Enter the non-reflecting b.c. menu.
    """

    fluent_name = "non-reflecting-bc"

    child_names = \
        ['general_nrbc', 'turbo_sepcific_nrbc']

    _child_classes = dict(
        general_nrbc=general_nrbc_cls,
        turbo_sepcific_nrbc=turbo_sepcific_nrbc_cls,
    )

