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

from .counter_clockwise import counter_clockwise as counter_clockwise_cls
class roll(Command):
    """
    Adjust the camera up-vector.
    
    Parameters
    ----------
        counter_clockwise : real
            'counter_clockwise' child.
    
    """

    fluent_name = "roll"

    argument_names = \
        ['counter_clockwise']

    _child_classes = dict(
        counter_clockwise=counter_clockwise_cls,
    )

