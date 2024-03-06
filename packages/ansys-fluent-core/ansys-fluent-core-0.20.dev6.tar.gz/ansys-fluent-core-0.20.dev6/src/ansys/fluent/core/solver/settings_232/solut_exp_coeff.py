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

from .option_10 import option as option_cls
from .value_1 import value as value_cls
class solut_exp_coeff(Group):
    """
    'solut_exp_coeff' child.
    """

    fluent_name = "solut-exp-coeff"

    child_names = \
        ['option', 'value']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
    )

