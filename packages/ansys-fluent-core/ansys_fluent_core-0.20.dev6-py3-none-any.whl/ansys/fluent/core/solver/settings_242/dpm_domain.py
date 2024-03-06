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

from .enabled_5 import enabled as enabled_cls
from .partitioning_method import partitioning_method as partitioning_method_cls
class dpm_domain(Group):
    """
    'dpm_domain' child.
    """

    fluent_name = "dpm-domain"

    child_names = \
        ['enabled', 'partitioning_method']

    _child_classes = dict(
        enabled=enabled_cls,
        partitioning_method=partitioning_method_cls,
    )

