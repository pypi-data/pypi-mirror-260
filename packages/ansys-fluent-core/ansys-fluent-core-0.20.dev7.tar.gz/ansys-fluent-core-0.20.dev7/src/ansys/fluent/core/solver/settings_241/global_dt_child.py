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

from .enable_pseudo_time_method import enable_pseudo_time_method as enable_pseudo_time_method_cls
from .pseudo_time_scale_factor import pseudo_time_scale_factor as pseudo_time_scale_factor_cls
from .implicit_under_relaxation_factor import implicit_under_relaxation_factor as implicit_under_relaxation_factor_cls
class global_dt_child(Group):
    """
    'child_object_type' of global_dt.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['enable_pseudo_time_method', 'pseudo_time_scale_factor',
         'implicit_under_relaxation_factor']

    _child_classes = dict(
        enable_pseudo_time_method=enable_pseudo_time_method_cls,
        pseudo_time_scale_factor=pseudo_time_scale_factor_cls,
        implicit_under_relaxation_factor=implicit_under_relaxation_factor_cls,
    )

