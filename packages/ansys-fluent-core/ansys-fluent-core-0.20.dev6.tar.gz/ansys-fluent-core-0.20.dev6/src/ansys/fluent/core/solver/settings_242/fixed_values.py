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

from .enable_12 import enable as enable_cls
from .cylindrical_fixed_var import cylindrical_fixed_var as cylindrical_fixed_var_cls
from .variables import variables as variables_cls
class fixed_values(Group):
    """
    Help not available.
    """

    fluent_name = "fixed-values"

    child_names = \
        ['enable', 'cylindrical_fixed_var', 'variables']

    _child_classes = dict(
        enable=enable_cls,
        cylindrical_fixed_var=cylindrical_fixed_var_cls,
        variables=variables_cls,
    )

