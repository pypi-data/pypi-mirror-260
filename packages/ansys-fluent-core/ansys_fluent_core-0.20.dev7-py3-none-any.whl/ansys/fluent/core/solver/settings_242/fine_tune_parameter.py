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

from .user_a import user_a as user_a_cls
from .user_e import user_e as user_e_cls
from .user_m import user_m as user_m_cls
from .user_n import user_n as user_n_cls
class fine_tune_parameter(Command):
    """
    Fine tune Arrhenius rate parameters.
    
    Parameters
    ----------
        user_a : real
            Specify fine-tuning parameter A in abuse model fitting.
        user_e : real
            Specify fine-tuning parameter E in abuse model fitting.
        user_m : real
            Specify fine-tuning parameter m in abuse model fitting.
        user_n : real
            Specify fine-tuning parameter n in abuse model fitting.
    
    """

    fluent_name = "fine-tune-parameter"

    argument_names = \
        ['user_a', 'user_e', 'user_m', 'user_n']

    _child_classes = dict(
        user_a=user_a_cls,
        user_e=user_e_cls,
        user_m=user_m_cls,
        user_n=user_n_cls,
    )

