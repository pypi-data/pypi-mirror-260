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

from .color_3 import color as color_cls
from .material import material as material_cls
class type_name_child(Group):
    """
    'child_object_type' of type_name.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['color', 'material']

    _child_classes = dict(
        color=color_cls,
        material=material_cls,
    )

