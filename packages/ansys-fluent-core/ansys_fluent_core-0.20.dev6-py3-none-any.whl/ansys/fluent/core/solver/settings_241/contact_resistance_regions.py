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
from .add_zone import add_zone as add_zone_cls
from .list_zone import list_zone as list_zone_cls
from .delete_zone import delete_zone as delete_zone_cls
from .contact_resis_child import contact_resis_child

class contact_resistance_regions(ListObject[contact_resis_child]):
    """
    Contact Resistance Regions.
    """

    fluent_name = "contact-resistance-regions"

    command_names = \
        ['list_properties', 'add_zone', 'list_zone', 'delete_zone']

    _child_classes = dict(
        list_properties=list_properties_cls,
        add_zone=add_zone_cls,
        list_zone=list_zone_cls,
        delete_zone=delete_zone_cls,
    )

    child_object_type: contact_resis_child = contact_resis_child
    """
    child_object_type of contact_resistance_regions.
    """
