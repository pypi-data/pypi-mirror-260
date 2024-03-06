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

from .data_type import data_type as data_type_cls
from .hw import hw as hw_cls
from .a import a as a_cls
from .e import e as e_cls
from .m import m as m_cls
from .n import n as n_cls
from .alpha0 import alpha0 as alpha0_cls
from .rate_table import rate_table as rate_table_cls
from .hw_table import hw_table as hw_table_cls
from .hw_udf import hw_udf as hw_udf_cls
from .udf_name import udf_name as udf_name_cls
class one_equation(Group):
    """
    'one_equation' child.
    """

    fluent_name = "one-equation"

    child_names = \
        ['data_type', 'hw', 'a', 'e', 'm', 'n', 'alpha0', 'rate_table',
         'hw_table', 'hw_udf', 'udf_name']

    _child_classes = dict(
        data_type=data_type_cls,
        hw=hw_cls,
        a=a_cls,
        e=e_cls,
        m=m_cls,
        n=n_cls,
        alpha0=alpha0_cls,
        rate_table=rate_table_cls,
        hw_table=hw_table_cls,
        hw_udf=hw_udf_cls,
        udf_name=udf_name_cls,
    )

