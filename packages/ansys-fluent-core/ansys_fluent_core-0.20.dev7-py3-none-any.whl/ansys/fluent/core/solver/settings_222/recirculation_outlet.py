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

from .change_type import change_type as change_type_cls
from .recirculation_outlet_child import recirculation_outlet_child

class recirculation_outlet(NamedObject[recirculation_outlet_child], _CreatableNamedObjectMixin[recirculation_outlet_child]):
    """
    'recirculation_outlet' child.
    """

    fluent_name = "recirculation-outlet"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: recirculation_outlet_child = recirculation_outlet_child
    """
    child_object_type of recirculation_outlet.
    """
