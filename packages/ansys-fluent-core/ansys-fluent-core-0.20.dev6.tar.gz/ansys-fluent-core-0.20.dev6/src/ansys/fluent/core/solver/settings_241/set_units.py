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

from .quantity import quantity as quantity_cls
from .units_name import units_name as units_name_cls
from .scale_factor import scale_factor as scale_factor_cls
from .offset_1 import offset as offset_cls
class set_units(Command):
    """
    Set unit conversion factors.
    
    Parameters
    ----------
        quantity : str
            'quantity' child.
        units_name : str
            'units_name' child.
        scale_factor : real
            'scale_factor' child.
        offset : real
            'offset' child.
    
    """

    fluent_name = "set-units"

    argument_names = \
        ['quantity', 'units_name', 'scale_factor', 'offset']

    _child_classes = dict(
        quantity=quantity_cls,
        units_name=units_name_cls,
        scale_factor=scale_factor_cls,
        offset=offset_cls,
    )

