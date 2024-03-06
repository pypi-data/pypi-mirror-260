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

from .apply_1 import apply as apply_cls
class use_fine_tune_parameter(Command):
    """
    Command to use fine-tuned parameters.
    
    Parameters
    ----------
        apply : bool
            Use fine-tuned parameters.
    
    """

    fluent_name = "use-fine-tune-parameter"

    argument_names = \
        ['apply']

    _child_classes = dict(
        apply=apply_cls,
    )

