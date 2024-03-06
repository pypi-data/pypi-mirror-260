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
from .rgp_table import rgp_table as rgp_table_cls
class molecular_weight(Group):
    """
    'molecular_weight' child.
    """

    fluent_name = "molecular-weight"

    child_names = \
        ['option', 'value', 'rgp_table']

    _child_classes = dict(
        option=option_cls,
        value=value_cls,
        rgp_table=rgp_table_cls,
    )

