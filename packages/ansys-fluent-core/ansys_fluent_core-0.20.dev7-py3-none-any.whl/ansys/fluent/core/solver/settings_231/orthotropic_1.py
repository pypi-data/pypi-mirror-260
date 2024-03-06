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

from .direction_0 import direction_0 as direction_0_cls
from .direction_1 import direction_1 as direction_1_cls
from .conductivity_0 import conductivity_0 as conductivity_0_cls
from .conductivity_1 import conductivity_1 as conductivity_1_cls
from .conductivity_2 import conductivity_2 as conductivity_2_cls
class orthotropic(Group):
    """
    'orthotropic' child.
    """

    fluent_name = "orthotropic"

    child_names = \
        ['direction_0', 'direction_1', 'conductivity_0', 'conductivity_1',
         'conductivity_2']

    _child_classes = dict(
        direction_0=direction_0_cls,
        direction_1=direction_1_cls,
        conductivity_0=conductivity_0_cls,
        conductivity_1=conductivity_1_cls,
        conductivity_2=conductivity_2_cls,
    )

