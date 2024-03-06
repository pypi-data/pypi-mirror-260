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

from .active import active as active_cls
from .min_value import min_value as min_value_cls
from .max_value import max_value as max_value_cls
from .min_transparency_value import min_transparency_value as min_transparency_value_cls
from .max_transparency_value import max_transparency_value as max_transparency_value_cls
class settings_child(Group):
    """
    'child_object_type' of settings.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['active', 'min_value', 'max_value', 'min_transparency_value',
         'max_transparency_value']

    _child_classes = dict(
        active=active_cls,
        min_value=min_value_cls,
        max_value=max_value_cls,
        min_transparency_value=min_transparency_value_cls,
        max_transparency_value=max_transparency_value_cls,
    )

