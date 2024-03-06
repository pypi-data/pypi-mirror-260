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

from .cell_zone_name import cell_zone_name as cell_zone_name_cls
class mrf_to_sliding_mesh(Command):
    """
    Change motion specification from MRF to moving mesh.
    
    Parameters
    ----------
        cell_zone_name : str
            Enter a cell zone name.
    
    """

    fluent_name = "mrf-to-sliding-mesh"

    argument_names = \
        ['cell_zone_name']

    _child_classes = dict(
        cell_zone_name=cell_zone_name_cls,
    )

