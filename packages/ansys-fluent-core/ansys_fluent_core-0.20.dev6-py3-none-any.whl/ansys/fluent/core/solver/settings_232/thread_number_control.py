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

from .thread_number_method import thread_number_method as thread_number_method_cls
from .fixed_thread_number import fixed_thread_number as fixed_thread_number_cls
class thread_number_control(Group):
    """
    Thread number control.
    """

    fluent_name = "thread-number-control"

    child_names = \
        ['thread_number_method', 'fixed_thread_number']

    _child_classes = dict(
        thread_number_method=thread_number_method_cls,
        fixed_thread_number=fixed_thread_number_cls,
    )

