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

from .autosave import autosave as autosave_cls
class calculation_activities(Group):
    """
    Enter the calculation activities menu.
    """

    fluent_name = "calculation-activities"

    command_names = \
        ['autosave']

    _child_classes = dict(
        autosave=autosave_cls,
    )

