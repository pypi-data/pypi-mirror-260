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

from .length import length as length_cls
from .boundary import boundary as boundary_cls
class knudsen_number_calculator(Command):
    """
    Utility to compute Kudsen number based on characteristic length and boundary information.
    
    Parameters
    ----------
        length : real
            Characteristic physics length.
        boundary : str
            Give flow boundary name.
    
    """

    fluent_name = "knudsen-number-calculator"

    argument_names = \
        ['length', 'boundary']

    _child_classes = dict(
        length=length_cls,
        boundary=boundary_cls,
    )

