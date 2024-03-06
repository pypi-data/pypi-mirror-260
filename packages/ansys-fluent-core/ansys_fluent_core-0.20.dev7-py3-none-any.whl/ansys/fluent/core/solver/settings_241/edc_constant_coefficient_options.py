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

from .volume_fraction_constant import volume_fraction_constant as volume_fraction_constant_cls
from .time_scale_constant import time_scale_constant as time_scale_constant_cls
class edc_constant_coefficient_options(Group):
    """
    'edc_constant_coefficient_options' child.
    """

    fluent_name = "edc-constant-coefficient-options"

    child_names = \
        ['volume_fraction_constant', 'time_scale_constant']

    _child_classes = dict(
        volume_fraction_constant=volume_fraction_constant_cls,
        time_scale_constant=time_scale_constant_cls,
    )

