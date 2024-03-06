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

from .smoothing_iteration import smoothing_iteration as smoothing_iteration_cls
class smooth_partition(Command):
    """
    Smooth partition interface.
    
    Parameters
    ----------
        smoothing_iteration : int
            Set maximum number of smoothing iterations.
    
    """

    fluent_name = "smooth-partition"

    argument_names = \
        ['smoothing_iteration']

    _child_classes = dict(
        smoothing_iteration=smoothing_iteration_cls,
    )

