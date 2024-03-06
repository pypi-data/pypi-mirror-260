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

from .impedance_2_child import impedance_2_child

class impedance_2(ListObject[impedance_2_child]):
    """
    'impedance_2' child.
    """

    fluent_name = "impedance-2"

    child_object_type: impedance_2_child = impedance_2_child
    """
    child_object_type of impedance_2.
    """
