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

from .pole import pole as pole_cls
from .amplitude import amplitude as amplitude_cls
class impedance_1_child(Group):
    """
    'child_object_type' of impedance_1.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['pole', 'amplitude']

    _child_classes = dict(
        pole=pole_cls,
        amplitude=amplitude_cls,
    )

