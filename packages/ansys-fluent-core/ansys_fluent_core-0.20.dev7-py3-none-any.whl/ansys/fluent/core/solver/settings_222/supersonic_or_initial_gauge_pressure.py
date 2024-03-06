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

from .option import option as option_cls
from .constant import constant as constant_cls
from .profile_name import profile_name as profile_name_cls
from .field_name import field_name as field_name_cls
from .udf import udf as udf_cls
class supersonic_or_initial_gauge_pressure(Group):
    """
    'supersonic_or_initial_gauge_pressure' child.
    """

    fluent_name = "supersonic-or-initial-gauge-pressure"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    _child_classes = dict(
        option=option_cls,
        constant=constant_cls,
        profile_name=profile_name_cls,
        field_name=field_name_cls,
        udf=udf_cls,
    )

