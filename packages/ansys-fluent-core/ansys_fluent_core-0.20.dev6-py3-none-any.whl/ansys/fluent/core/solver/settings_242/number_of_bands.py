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

from .on_all_interfaces import on_all_interfaces as on_all_interfaces_cls
from .on_specified_interface import on_specified_interface as on_specified_interface_cls
class number_of_bands(Group):
    """
    Specify maximum number of bands to be employed at the mixing plane interface.
    """

    fluent_name = "number-of-bands"

    command_names = \
        ['on_all_interfaces', 'on_specified_interface']

    _child_classes = dict(
        on_all_interfaces=on_all_interfaces_cls,
        on_specified_interface=on_specified_interface_cls,
    )

