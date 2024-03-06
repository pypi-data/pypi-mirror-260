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

from .set_units import set_units as set_units_cls
from .set_unit_system import set_unit_system as set_unit_system_cls
class units(Group):
    """
    'units' child.
    """

    fluent_name = "units"

    command_names = \
        ['set_units', 'set_unit_system']

    _child_classes = dict(
        set_units=set_units_cls,
        set_unit_system=set_unit_system_cls,
    )

