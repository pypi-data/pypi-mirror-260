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

from .enable_7 import enable as enable_cls
from .time_delay import time_delay as time_delay_cls
class particle_reinjector(Group):
    """
    'particle_reinjector' child.
    """

    fluent_name = "particle-reinjector"

    child_names = \
        ['enable', 'time_delay']

    _child_classes = dict(
        enable=enable_cls,
        time_delay=time_delay_cls,
    )

