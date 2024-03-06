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

from .field import field as field_cls
from .data_source import data_source as data_source_cls
from .range_options import range_options as range_options_cls
from .color_density import color_density as color_density_cls
from .color_map import color_map as color_map_cls
from .cell_zones_3 import cell_zones as cell_zones_cls
class home_options(Group):
    """
    'home_options' child.
    """

    fluent_name = "home-options"

    child_names = \
        ['field', 'data_source', 'range_options', 'color_density',
         'color_map', 'cell_zones']

    _child_classes = dict(
        field=field_cls,
        data_source=data_source_cls,
        range_options=range_options_cls,
        color_density=color_density_cls,
        color_map=color_map_cls,
        cell_zones=cell_zones_cls,
    )

