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

from .enable import enable as enable_cls
from .gradient_correction_mode import gradient_correction_mode as gradient_correction_mode_cls
class enable(Command):
    """
    Enable Warped-Face Gradient Correction.
    
    Parameters
    ----------
        enable : bool
            'enable' child.
        gradient_correction_mode : str
            'gradient_correction_mode' child.
    
    """

    fluent_name = "enable?"

    argument_names = \
        ['enable', 'gradient_correction_mode']

    _child_classes = dict(
        enable=enable_cls,
        gradient_correction_mode=gradient_correction_mode_cls,
    )

