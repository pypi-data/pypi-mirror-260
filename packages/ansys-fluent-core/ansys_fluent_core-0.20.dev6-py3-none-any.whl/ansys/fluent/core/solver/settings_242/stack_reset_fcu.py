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

from .reset import reset as reset_cls
class stack_reset_fcu(Command):
    """
    Reset stack units.
    
    Parameters
    ----------
        reset : bool
            'reset' child.
    
    """

    fluent_name = "stack-reset-fcu"

    argument_names = \
        ['reset']

    _child_classes = dict(
        reset=reset_cls,
    )

