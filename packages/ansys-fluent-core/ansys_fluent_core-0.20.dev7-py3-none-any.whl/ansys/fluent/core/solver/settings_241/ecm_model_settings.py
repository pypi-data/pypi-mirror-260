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

from .initial_soc import initial_soc as initial_soc_cls
from .ref_capacity import ref_capacity as ref_capacity_cls
from .two_set_data import two_set_data as two_set_data_cls
from .data_type import data_type as data_type_cls
from .chen_rs import chen_rs as chen_rs_cls
from .chen_r1 import chen_r1 as chen_r1_cls
from .chen_c1 import chen_c1 as chen_c1_cls
from .chen_r2 import chen_r2 as chen_r2_cls
from .chen_c2 import chen_c2 as chen_c2_cls
from .chen_voc import chen_voc as chen_voc_cls
from .chen_rs_c import chen_rs_c as chen_rs_c_cls
from .chen_r1_c import chen_r1_c as chen_r1_c_cls
from .chen_c1_c import chen_c1_c as chen_c1_c_cls
from .chen_r2_c import chen_r2_c as chen_r2_c_cls
from .chen_c2_c import chen_c2_c as chen_c2_c_cls
from .chen_voc_c import chen_voc_c as chen_voc_c_cls
from .poly_rs import poly_rs as poly_rs_cls
from .poly_r1 import poly_r1 as poly_r1_cls
from .poly_c1 import poly_c1 as poly_c1_cls
from .poly_r2 import poly_r2 as poly_r2_cls
from .poly_c2 import poly_c2 as poly_c2_cls
from .poly_voc import poly_voc as poly_voc_cls
from .poly_rs_c import poly_rs_c as poly_rs_c_cls
from .poly_r1_c import poly_r1_c as poly_r1_c_cls
from .poly_c1_c import poly_c1_c as poly_c1_c_cls
from .poly_r2_c import poly_r2_c as poly_r2_c_cls
from .poly_c2_c import poly_c2_c as poly_c2_c_cls
from .poly_voc_c import poly_voc_c as poly_voc_c_cls
from .table_rs import table_rs as table_rs_cls
from .table_r1 import table_r1 as table_r1_cls
from .table_c1 import table_c1 as table_c1_cls
from .table_r2 import table_r2 as table_r2_cls
from .table_c2 import table_c2 as table_c2_cls
from .table_r3 import table_r3 as table_r3_cls
from .table_c3 import table_c3 as table_c3_cls
from .table_voc import table_voc as table_voc_cls
from .table_rs_c import table_rs_c as table_rs_c_cls
from .table_r1_c import table_r1_c as table_r1_c_cls
from .table_c1_c import table_c1_c as table_c1_c_cls
from .table_r2_c import table_r2_c as table_r2_c_cls
from .table_c2_c import table_c2_c as table_c2_c_cls
from .table_r3_c import table_r3_c as table_r3_c_cls
from .table_c3_c import table_c3_c as table_c3_c_cls
from .table_voc_c import table_voc_c as table_voc_c_cls
class ecm_model_settings(Group):
    """
    'ecm_model_settings' child.
    """

    fluent_name = "ecm-model-settings"

    child_names = \
        ['initial_soc', 'ref_capacity', 'two_set_data', 'data_type',
         'chen_rs', 'chen_r1', 'chen_c1', 'chen_r2', 'chen_c2', 'chen_voc',
         'chen_rs_c', 'chen_r1_c', 'chen_c1_c', 'chen_r2_c', 'chen_c2_c',
         'chen_voc_c', 'poly_rs', 'poly_r1', 'poly_c1', 'poly_r2', 'poly_c2',
         'poly_voc', 'poly_rs_c', 'poly_r1_c', 'poly_c1_c', 'poly_r2_c',
         'poly_c2_c', 'poly_voc_c', 'table_rs', 'table_r1', 'table_c1',
         'table_r2', 'table_c2', 'table_r3', 'table_c3', 'table_voc',
         'table_rs_c', 'table_r1_c', 'table_c1_c', 'table_r2_c', 'table_c2_c',
         'table_r3_c', 'table_c3_c', 'table_voc_c']

    _child_classes = dict(
        initial_soc=initial_soc_cls,
        ref_capacity=ref_capacity_cls,
        two_set_data=two_set_data_cls,
        data_type=data_type_cls,
        chen_rs=chen_rs_cls,
        chen_r1=chen_r1_cls,
        chen_c1=chen_c1_cls,
        chen_r2=chen_r2_cls,
        chen_c2=chen_c2_cls,
        chen_voc=chen_voc_cls,
        chen_rs_c=chen_rs_c_cls,
        chen_r1_c=chen_r1_c_cls,
        chen_c1_c=chen_c1_c_cls,
        chen_r2_c=chen_r2_c_cls,
        chen_c2_c=chen_c2_c_cls,
        chen_voc_c=chen_voc_c_cls,
        poly_rs=poly_rs_cls,
        poly_r1=poly_r1_cls,
        poly_c1=poly_c1_cls,
        poly_r2=poly_r2_cls,
        poly_c2=poly_c2_cls,
        poly_voc=poly_voc_cls,
        poly_rs_c=poly_rs_c_cls,
        poly_r1_c=poly_r1_c_cls,
        poly_c1_c=poly_c1_c_cls,
        poly_r2_c=poly_r2_c_cls,
        poly_c2_c=poly_c2_c_cls,
        poly_voc_c=poly_voc_c_cls,
        table_rs=table_rs_cls,
        table_r1=table_r1_cls,
        table_c1=table_c1_cls,
        table_r2=table_r2_cls,
        table_c2=table_c2_cls,
        table_r3=table_r3_cls,
        table_c3=table_c3_cls,
        table_voc=table_voc_cls,
        table_rs_c=table_rs_c_cls,
        table_r1_c=table_r1_c_cls,
        table_c1_c=table_c1_c_cls,
        table_r2_c=table_r2_c_cls,
        table_c2_c=table_c2_c_cls,
        table_r3_c=table_r3_c_cls,
        table_c3_c=table_c3_c_cls,
        table_voc_c=table_voc_c_cls,
    )

