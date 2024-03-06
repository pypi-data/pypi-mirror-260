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

from .sc_enable_sub_stepping_option_per_coupling_step import sc_enable_sub_stepping_option_per_coupling_step as sc_enable_sub_stepping_option_per_coupling_step_cls
class unsteady_statistics(Group):
    """
    Enter the unsteady statistics menu.
    """

    fluent_name = "unsteady-statistics"

    command_names = \
        ['sc_enable_sub_stepping_option_per_coupling_step']

    _child_classes = dict(
        sc_enable_sub_stepping_option_per_coupling_step=sc_enable_sub_stepping_option_per_coupling_step_cls,
    )

