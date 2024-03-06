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

from .name_1 import name as name_cls
from .old_props import old_props as old_props_cls
from .file_name_2 import file_name as file_name_cls
from .frequency import frequency as frequency_cls
from .flow_frequency import flow_frequency as flow_frequency_cls
from .itr_index import itr_index as itr_index_cls
from .run_index import run_index as run_index_cls
from .frequency_of import frequency_of as frequency_of_cls
from .report_defs import report_defs as report_defs_cls
from .print_2 import print as print_cls
from .active import active as active_cls
from .write_instantaneous_values import write_instantaneous_values as write_instantaneous_values_cls
class report_files_child(Group):
    """
    'child_object_type' of report_files.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'old_props', 'file_name', 'frequency', 'flow_frequency',
         'itr_index', 'run_index', 'frequency_of', 'report_defs', 'print',
         'active', 'write_instantaneous_values']

    _child_classes = dict(
        name=name_cls,
        old_props=old_props_cls,
        file_name=file_name_cls,
        frequency=frequency_cls,
        flow_frequency=flow_frequency_cls,
        itr_index=itr_index_cls,
        run_index=run_index_cls,
        frequency_of=frequency_of_cls,
        report_defs=report_defs_cls,
        print=print_cls,
        active=active_cls,
        write_instantaneous_values=write_instantaneous_values_cls,
    )

