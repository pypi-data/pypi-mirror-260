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

from .solution_controls import solution_controls as solution_controls_cls
from .tolerance_1 import tolerance as tolerance_cls
from .convert_to_mapped_interface import convert_to_mapped_interface as convert_to_mapped_interface_cls
class mapped_interface_options(Group):
    """
    Enter the mapped-interface-options menu.
    """

    fluent_name = "mapped-interface-options"

    command_names = \
        ['solution_controls', 'tolerance', 'convert_to_mapped_interface']

    _child_classes = dict(
        solution_controls=solution_controls_cls,
        tolerance=tolerance_cls,
        convert_to_mapped_interface=convert_to_mapped_interface_cls,
    )

