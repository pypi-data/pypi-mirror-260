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

from .heat_exchanger import heat_exchanger as heat_exchanger_cls
from .fluid_zone import fluid_zone as fluid_zone_cls
from .boundary_zone import boundary_zone as boundary_zone_cls
from .report_type import report_type as report_type_cls
from .write_to_file import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_file import append_file as append_file_cls
from .overwrite import overwrite as overwrite_cls
class mass_flow_rate(Command):
    """
    'mass_flow_rate' command.
    
    Parameters
    ----------
        heat_exchanger : str
            'heat_exchanger' child.
        fluid_zone : str
            'fluid_zone' child.
        boundary_zone : str
            'boundary_zone' child.
        report_type : str
            'report_type' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append_file : bool
            'append_file' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "mass-flow-rate"

    argument_names = \
        ['heat_exchanger', 'fluid_zone', 'boundary_zone', 'report_type',
         'write_to_file', 'file_name', 'append_file', 'overwrite']

    _child_classes = dict(
        heat_exchanger=heat_exchanger_cls,
        fluid_zone=fluid_zone_cls,
        boundary_zone=boundary_zone_cls,
        report_type=report_type_cls,
        write_to_file=write_to_file_cls,
        file_name=file_name_cls,
        append_file=append_file_cls,
        overwrite=overwrite_cls,
    )

