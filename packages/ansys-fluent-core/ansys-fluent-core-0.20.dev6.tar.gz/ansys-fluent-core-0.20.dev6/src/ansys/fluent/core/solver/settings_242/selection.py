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

from .adjoint_observable import adjoint_observable as adjoint_observable_cls
from .evaluate import evaluate as evaluate_cls
from .write_to_file_3 import write_to_file as write_to_file_cls
class selection(Group):
    """
    Observable selection menu.
    """

    fluent_name = "selection"

    child_names = \
        ['adjoint_observable']

    command_names = \
        ['evaluate', 'write_to_file']

    _child_classes = dict(
        adjoint_observable=adjoint_observable_cls,
        evaluate=evaluate_cls,
        write_to_file=write_to_file_cls,
    )

