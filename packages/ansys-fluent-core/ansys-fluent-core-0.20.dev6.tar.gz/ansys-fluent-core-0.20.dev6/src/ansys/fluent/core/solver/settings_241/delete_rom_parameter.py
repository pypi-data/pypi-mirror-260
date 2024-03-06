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

from .parameter_names import parameter_names as parameter_names_cls
class delete_rom_parameter(Command):
    """
    Delete ROM-related paramters.
    
    Parameters
    ----------
        parameter_names : typing.List[str]
            Set deleted parameter lists.
    
    """

    fluent_name = "delete-rom-parameter"

    argument_names = \
        ['parameter_names']

    _child_classes = dict(
        parameter_names=parameter_names_cls,
    )

