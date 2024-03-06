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

from .enabled_19 import enabled as enabled_cls
from .h import h as h_cls
from .a_1 import a as a_cls
from .e_1 import e as e_cls
from .trigger_t import trigger_t as trigger_t_cls
from .e0_1 import e0 as e0_cls
class internal_short(Group):
    """
    Set internal short reaction kinetics.
    """

    fluent_name = "internal-short"

    child_names = \
        ['enabled', 'h', 'a', 'e', 'trigger_t', 'e0']

    _child_classes = dict(
        enabled=enabled_cls,
        h=h_cls,
        a=a_cls,
        e=e_cls,
        trigger_t=trigger_t_cls,
        e0=e0_cls,
    )

