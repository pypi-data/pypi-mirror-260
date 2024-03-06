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

from .repair_angle import repair_angle as repair_angle_cls
from .periodic_input import periodic_input as periodic_input_cls
from .angle_input import angle_input as angle_input_cls
from .repair_periodic import repair_periodic as repair_periodic_cls
class repair_periodic(Command):
    """
    Modify mesh to enforce specified periodic rotation angle.
    
    Parameters
    ----------
        repair_angle : bool
            'repair_angle' child.
        periodic_input : str
            Enter id/name of zone to repair.
        angle_input : real
            Enter desired angle of rotation in degrees.
        repair_periodic : bool
            'repair_periodic' child.
    
    """

    fluent_name = "repair-periodic"

    argument_names = \
        ['repair_angle', 'periodic_input', 'angle_input', 'repair_periodic']

    _child_classes = dict(
        repair_angle=repair_angle_cls,
        periodic_input=periodic_input_cls,
        angle_input=angle_input_cls,
        repair_periodic=repair_periodic_cls,
    )

