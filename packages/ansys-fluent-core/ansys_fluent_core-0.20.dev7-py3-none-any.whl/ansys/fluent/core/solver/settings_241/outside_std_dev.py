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

from .lower import lower as lower_cls
from .upper import upper as upper_cls
class outside_std_dev(Group):
    """
    'outside_std_dev' child.
    """

    fluent_name = "outside-std-dev"

    child_names = \
        ['lower', 'upper']

    _child_classes = dict(
        lower=lower_cls,
        upper=upper_cls,
    )

