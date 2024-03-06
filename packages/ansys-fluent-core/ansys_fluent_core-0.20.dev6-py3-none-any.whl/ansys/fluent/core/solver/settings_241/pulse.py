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

from .pulse_mode import pulse_mode as pulse_mode_cls
from .write_2 import write as write_cls
class pulse(Group):
    """
    Enter save pathline/particle tracks pulse menu.
    """

    fluent_name = "pulse"

    child_names = \
        ['pulse_mode']

    command_names = \
        ['write']

    _child_classes = dict(
        pulse_mode=pulse_mode_cls,
        write=write_cls,
    )

