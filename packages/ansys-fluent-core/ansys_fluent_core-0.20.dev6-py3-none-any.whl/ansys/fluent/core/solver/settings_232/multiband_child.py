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

from .start_1 import start as start_cls
from .end import end as end_cls
class multiband_child(Group):
    """
    'child_object_type' of multiband.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['start', 'end']

    _child_classes = dict(
        start=start_cls,
        end=end_cls,
    )

