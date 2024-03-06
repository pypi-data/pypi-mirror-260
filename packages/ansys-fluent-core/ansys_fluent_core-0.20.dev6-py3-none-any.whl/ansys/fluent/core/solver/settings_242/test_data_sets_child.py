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

from .filename_3 import filename as filename_cls
from .initial_alpha import initial_alpha as initial_alpha_cls
from .initial_temp import initial_temp as initial_temp_cls
from .ambient_temp import ambient_temp as ambient_temp_cls
from .external_ht_coeff import external_ht_coeff as external_ht_coeff_cls
from .enclosure_temp import enclosure_temp as enclosure_temp_cls
from .include_max_temp_enabled import include_max_temp_enabled as include_max_temp_enabled_cls
from .range_temp import range_temp as range_temp_cls
class test_data_sets_child(Group):
    """
    'child_object_type' of test_data_sets.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['filename', 'initial_alpha', 'initial_temp', 'ambient_temp',
         'external_ht_coeff', 'enclosure_temp', 'include_max_temp_enabled',
         'range_temp']

    _child_classes = dict(
        filename=filename_cls,
        initial_alpha=initial_alpha_cls,
        initial_temp=initial_temp_cls,
        ambient_temp=ambient_temp_cls,
        external_ht_coeff=external_ht_coeff_cls,
        enclosure_temp=enclosure_temp_cls,
        include_max_temp_enabled=include_max_temp_enabled_cls,
        range_temp=range_temp_cls,
    )

