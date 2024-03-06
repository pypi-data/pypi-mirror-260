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

from .f_length import f_length as f_length_cls
from .re_theta_c import re_theta_c as re_theta_c_cls
from .re_theta_t import re_theta_t as re_theta_t_cls
class user_defined_transition(Group):
    """
    Set user-defined transition correlations.
    """

    fluent_name = "user-defined-transition"

    child_names = \
        ['f_length', 're_theta_c', 're_theta_t']

    _child_classes = dict(
        f_length=f_length_cls,
        re_theta_c=re_theta_c_cls,
        re_theta_t=re_theta_t_cls,
    )

