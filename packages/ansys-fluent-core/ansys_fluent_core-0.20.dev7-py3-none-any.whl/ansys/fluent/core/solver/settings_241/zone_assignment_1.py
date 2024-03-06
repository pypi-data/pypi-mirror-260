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

from .active_zone import active_zone as active_zone_cls
from .passive_zone import passive_zone as passive_zone_cls
from .positive_tab import positive_tab as positive_tab_cls
from .negative_tab import negative_tab as negative_tab_cls
from .virtual_connection import virtual_connection as virtual_connection_cls
from .print_battery_connection import print_battery_connection as print_battery_connection_cls
class zone_assignment(Group):
    """
    'zone_assignment' child.
    """

    fluent_name = "zone-assignment"

    child_names = \
        ['active_zone', 'passive_zone', 'positive_tab', 'negative_tab']

    command_names = \
        ['virtual_connection', 'print_battery_connection']

    _child_classes = dict(
        active_zone=active_zone_cls,
        passive_zone=passive_zone_cls,
        positive_tab=positive_tab_cls,
        negative_tab=negative_tab_cls,
        virtual_connection=virtual_connection_cls,
        print_battery_connection=print_battery_connection_cls,
    )

