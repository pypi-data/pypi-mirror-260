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

from .interface_number import interface_number as interface_number_cls
from .bands import bands as bands_cls
class set_specific_interface(Command):
    """
    Set number of band to be used for mixing.
    
    Parameters
    ----------
        interface_number : int
            Set number of band to be used for mixing.
        bands : int
            Set number of band to be used for mixing.
    
    """

    fluent_name = "set-specific-interface"

    argument_names = \
        ['interface_number', 'bands']

    _child_classes = dict(
        interface_number=interface_number_cls,
        bands=bands_cls,
    )

