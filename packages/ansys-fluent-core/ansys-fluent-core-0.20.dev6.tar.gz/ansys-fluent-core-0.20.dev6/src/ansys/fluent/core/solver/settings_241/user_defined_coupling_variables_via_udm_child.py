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

from .udm_index import udm_index as udm_index_cls
from .zone_names_6 import zone_names as zone_names_cls
from .extensive import extensive as extensive_cls
from .input import input as input_cls
from .output_1 import output as output_cls
from .output_variable_name import output_variable_name as output_variable_name_cls
from .input_variable_name import input_variable_name as input_variable_name_cls
class user_defined_coupling_variables_via_udm_child(Group):
    """
    'child_object_type' of user_defined_coupling_variables_via_udm.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['udm_index', 'zone_names', 'extensive', 'input', 'output',
         'output_variable_name', 'input_variable_name']

    _child_classes = dict(
        udm_index=udm_index_cls,
        zone_names=zone_names_cls,
        extensive=extensive_cls,
        input=input_cls,
        output=output_cls,
        output_variable_name=output_variable_name_cls,
        input_variable_name=input_variable_name_cls,
    )

