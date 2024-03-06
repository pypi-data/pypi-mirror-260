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
from .translate import translate as translate_cls
from .rotation_angle import rotation_angle as rotation_angle_cls
from .offset import offset as offset_cls
from .axis import axis as axis_cls
class copy_move_cell_zone(Command):
    """
    Copy and translate or rotate a cell zone.
    
    Parameters
    ----------
        cell_zone_name : str
            Enter a cell zone name.
        translate : bool
            Specify if copied zone should be translated (#t) or rotated (#f).
        rotation_angle : real
            'rotation_angle' child.
        offset : typing.List[real]
            'offset' child.
        axis : typing.List[real]
            'axis' child.
    
    """

    fluent_name = "copy-move-cell-zone"

    argument_names = \
        ['cell_zone_name', 'translate', 'rotation_angle', 'offset', 'axis']

    _child_classes = dict(
        cell_zone_name=cell_zone_name_cls,
        translate=translate_cls,
        rotation_angle=rotation_angle_cls,
        offset=offset_cls,
        axis=axis_cls,
    )

