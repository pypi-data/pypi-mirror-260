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

from .file_name_1 import file_name as file_name_cls
from .cell_func_domain_export import cell_func_domain_export as cell_func_domain_export_cls
from .binary_format import binary_format as binary_format_cls
from .cellzones import cellzones as cellzones_cls
from .interior_zone_surfaces import interior_zone_surfaces as interior_zone_surfaces_cls
from .cell_centered import cell_centered as cell_centered_cls
class ensight_gold(Command):
    """
    Write EnSight Gold geometry, velocity, and scalar files.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        cell_func_domain_export : typing.List[str]
            'cell_func_domain_export' child.
        binary_format : bool
            'binary_format' child.
        cellzones : typing.List[str]
            List of cell zones to export.
        interior_zone_surfaces : typing.List[str]
            List of surfaces to export.
        cell_centered : bool
            'cell_centered' child.
    
    """

    fluent_name = "ensight-gold"

    argument_names = \
        ['file_name', 'cell_func_domain_export', 'binary_format', 'cellzones',
         'interior_zone_surfaces', 'cell_centered']

    _child_classes = dict(
        file_name=file_name_cls,
        cell_func_domain_export=cell_func_domain_export_cls,
        binary_format=binary_format_cls,
        cellzones=cellzones_cls,
        interior_zone_surfaces=interior_zone_surfaces_cls,
        cell_centered=cell_centered_cls,
    )

