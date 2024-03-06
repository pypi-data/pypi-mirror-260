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

from .name_2 import name as name_cls
from .field import field as field_cls
from .surface_2 import surface as surface_cls
from .zone_1 import zone as zone_cls
from .min import min as min_cls
from .max import max as max_cls
from .iso_value import iso_value as iso_value_cls
class iso_surface_child(Group):
    """
    'child_object_type' of iso_surface.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'field', 'surface', 'zone', 'min', 'max', 'iso_value']

    _child_classes = dict(
        name=name_cls,
        field=field_cls,
        surface=surface_cls,
        zone=zone_cls,
        min=min_cls,
        max=max_cls,
        iso_value=iso_value_cls,
    )

