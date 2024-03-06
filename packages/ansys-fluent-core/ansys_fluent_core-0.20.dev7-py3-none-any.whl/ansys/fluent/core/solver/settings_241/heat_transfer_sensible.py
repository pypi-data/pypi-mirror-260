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

from .domain import domain as domain_cls
from .all_boundary_zones import all_boundary_zones as all_boundary_zones_cls
from .zones_1 import zones as zones_cls
from .physics_1 import physics as physics_cls
from .write_to_file_1 import write_to_file as write_to_file_cls
from .file_name_1 import file_name as file_name_cls
from .append_data import append_data as append_data_cls
class heat_transfer_sensible(Command):
    """
    Print sensible heat transfer rate at boundaries.
    
    Parameters
    ----------
        domain : str
            'domain' child.
        all_boundary_zones : bool
            Select all the boundary/interior zones.
        zones : typing.List[str]
            Enter zone name list.
        physics : typing.List[str]
            'physics' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append_data : bool
            'append_data' child.
    
    """

    fluent_name = "heat-transfer-sensible"

    argument_names = \
        ['domain', 'all_boundary_zones', 'zones', 'physics', 'write_to_file',
         'file_name', 'append_data']

    _child_classes = dict(
        domain=domain_cls,
        all_boundary_zones=all_boundary_zones_cls,
        zones=zones_cls,
        physics=physics_cls,
        write_to_file=write_to_file_cls,
        file_name=file_name_cls,
        append_data=append_data_cls,
    )

