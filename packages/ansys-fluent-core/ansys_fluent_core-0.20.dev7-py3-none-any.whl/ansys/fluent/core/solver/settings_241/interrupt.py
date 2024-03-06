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

from .interrupt_at import interrupt_at as interrupt_at_cls
class interrupt(Command):
    """
    Interrupt the iterations.
    
    Parameters
    ----------
        interrupt_at : str
            Select when should the solution be interrupted.
    
    """

    fluent_name = "interrupt"

    argument_names = \
        ['interrupt_at']

    _child_classes = dict(
        interrupt_at=interrupt_at_cls,
    )

