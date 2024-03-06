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

from .enabled_29 import enabled as enabled_cls
from .coolant_zone_list import coolant_zone_list as coolant_zone_list_cls
from .coolant_density import coolant_density as coolant_density_cls
class coolant_channel(Group):
    """
    Set up coolant channel.
    """

    fluent_name = "coolant-channel"

    child_names = \
        ['enabled', 'coolant_zone_list', 'coolant_density']

    _child_classes = dict(
        enabled=enabled_cls,
        coolant_zone_list=coolant_zone_list_cls,
        coolant_density=coolant_density_cls,
    )

