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

from .enforce_flux_scaling import enforce_flux_scaling as enforce_flux_scaling_cls
from .print_settings import print_settings as print_settings_cls
class expert(Group):
    """
    Set the expert parameters for turbo interfaces.
    """

    fluent_name = "expert"

    command_names = \
        ['enforce_flux_scaling', 'print_settings']

    _child_classes = dict(
        enforce_flux_scaling=enforce_flux_scaling_cls,
        print_settings=print_settings_cls,
    )

