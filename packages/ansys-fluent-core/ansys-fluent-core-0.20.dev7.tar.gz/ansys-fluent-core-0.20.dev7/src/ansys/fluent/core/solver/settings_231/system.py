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

from .proc_statistics import proc_statistics as proc_statistics_cls
from .sys_statistics import sys_statistics as sys_statistics_cls
from .gpgpu_statistics import gpgpu_statistics as gpgpu_statistics_cls
from .time_statistics import time_statistics as time_statistics_cls
class system(Group):
    """
    'system' child.
    """

    fluent_name = "system"

    command_names = \
        ['proc_statistics', 'sys_statistics', 'gpgpu_statistics',
         'time_statistics']

    _child_classes = dict(
        proc_statistics=proc_statistics_cls,
        sys_statistics=sys_statistics_cls,
        gpgpu_statistics=gpgpu_statistics_cls,
        time_statistics=time_statistics_cls,
    )

