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

from .list_properties import list_properties as list_properties_cls
from .resize import resize as resize_cls
from .add_zone_1 import add_zone as add_zone_cls
from .list_zone_1 import list_zone as list_zone_cls
from .delete_zone_2 import delete_zone as delete_zone_cls
from .contact_resistance_child import contact_resistance_child

class contact_resistance_regions(ListObject[contact_resistance_child]):
    """
    Setup contact surfaces and resistance.
    """

    fluent_name = "contact-resistance-regions"

    command_names = \
        ['list_properties', 'resize', 'add_zone', 'list_zone', 'delete_zone']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
        add_zone=add_zone_cls,
        list_zone=list_zone_cls,
        delete_zone=delete_zone_cls,
    )

    child_object_type: contact_resistance_child = contact_resistance_child
    """
    child_object_type of contact_resistance_regions.
    """
