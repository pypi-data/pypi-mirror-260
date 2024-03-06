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

from .enable_in_tui import enable_in_tui as enable_in_tui_cls
from .input_parameters_1 import input_parameters as input_parameters_cls
from .output_parameters_1 import output_parameters as output_parameters_cls
class parameters(Group):
    """
    'parameters' child.
    """

    fluent_name = "parameters"

    child_names = \
        ['enable_in_tui', 'input_parameters', 'output_parameters']

    _child_classes = dict(
        enable_in_tui=enable_in_tui_cls,
        input_parameters=input_parameters_cls,
        output_parameters=output_parameters_cls,
    )

