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

from .name import name as name_cls
from .field_1 import field as field_cls
from .surfaces_5 import surfaces as surfaces_cls
from .zones_4 import zones as zones_cls
from .min_3 import min as min_cls
from .max_3 import max as max_cls
from .iso_values import iso_values as iso_values_cls
from .display_4 import display as display_cls
class iso_surface_child(Group):
    """
    'child_object_type' of iso_surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'field', 'surfaces', 'zones', 'min', 'max', 'iso_values']

    command_names = \
        ['display']

    _child_classes = dict(
        name=name_cls,
        field=field_cls,
        surfaces=surfaces_cls,
        zones=zones_cls,
        min=min_cls,
        max=max_cls,
        iso_values=iso_values_cls,
        display=display_cls,
    )

