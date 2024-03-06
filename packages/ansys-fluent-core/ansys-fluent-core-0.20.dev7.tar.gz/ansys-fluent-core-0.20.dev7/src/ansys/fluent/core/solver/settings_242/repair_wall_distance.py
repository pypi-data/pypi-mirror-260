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

from .repair_1 import repair as repair_cls
class repair_wall_distance(Command):
    """
    Correct wall distance at very high aspect ratio hexahedral/polyhedral cells.
    
    Parameters
    ----------
        repair : bool
            'repair' child.
    
    """

    fluent_name = "repair-wall-distance"

    argument_names = \
        ['repair']

    _child_classes = dict(
        repair=repair_cls,
    )

