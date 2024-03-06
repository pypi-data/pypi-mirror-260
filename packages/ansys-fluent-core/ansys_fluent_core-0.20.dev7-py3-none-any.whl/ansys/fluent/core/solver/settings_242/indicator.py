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

from .indicator_type import indicator_type as indicator_type_cls
from .single_scalar_fn import single_scalar_fn as single_scalar_fn_cls
from .multi_scalar_fn import multi_scalar_fn as multi_scalar_fn_cls
class indicator(Group):
    """
    Set the indicator type and variable(s) for anisotropic adaption.
    """

    fluent_name = "indicator"

    child_names = \
        ['indicator_type', 'single_scalar_fn', 'multi_scalar_fn']

    _child_classes = dict(
        indicator_type=indicator_type_cls,
        single_scalar_fn=single_scalar_fn_cls,
        multi_scalar_fn=multi_scalar_fn_cls,
    )

