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

from .use import use as use_cls
from .threshold import threshold as threshold_cls
class mesh_adaption(Group):
    """
    Use load balancing for mesh adaption?.
    """

    fluent_name = "mesh-adaption"

    child_names = \
        ['use', 'threshold']

    _child_classes = dict(
        use=use_cls,
        threshold=threshold_cls,
    )

