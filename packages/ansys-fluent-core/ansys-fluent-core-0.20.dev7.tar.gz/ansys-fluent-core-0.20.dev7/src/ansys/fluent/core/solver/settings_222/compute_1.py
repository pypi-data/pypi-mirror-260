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

from .compute import compute as compute_cls
class compute(Group):
    """
    'compute' child.
    """

    fluent_name = "compute"

    child_names = \
        ['compute']

    _child_classes = dict(
        compute=compute_cls,
    )

