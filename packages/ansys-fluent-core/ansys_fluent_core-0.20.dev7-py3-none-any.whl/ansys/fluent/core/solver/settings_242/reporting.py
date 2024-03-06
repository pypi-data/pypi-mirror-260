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

from .boundary_choice import boundary_choice as boundary_choice_cls
from .report_3 import report as report_cls
from .write_to_file_4 import write_to_file as write_to_file_cls
class reporting(Group):
    """
    Adjoint reporting menu.
    """

    fluent_name = "reporting"

    child_names = \
        ['boundary_choice']

    command_names = \
        ['report', 'write_to_file']

    _child_classes = dict(
        boundary_choice=boundary_choice_cls,
        report=report_cls,
        write_to_file=write_to_file_cls,
    )

