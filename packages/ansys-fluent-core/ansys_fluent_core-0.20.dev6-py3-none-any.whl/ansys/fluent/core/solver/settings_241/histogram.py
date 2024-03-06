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

from .cell_function_1 import cell_function as cell_function_cls
from .auto_range_2 import auto_range as auto_range_cls
from .minimum_1 import minimum as minimum_cls
from .maximum_1 import maximum as maximum_cls
from .num_divisions import num_divisions as num_divisions_cls
from .all_zones import all_zones as all_zones_cls
from .zones_1 import zones as zones_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .print_4 import print as print_cls
from .plot_5 import plot as plot_cls
from .write_3 import write as write_cls
class histogram(Group):
    """
    'histogram' child.
    """

    fluent_name = "histogram"

    child_names = \
        ['cell_function', 'auto_range', 'minimum', 'maximum', 'num_divisions',
         'all_zones', 'zones', 'axes', 'curves']

    command_names = \
        ['print', 'plot', 'write']

    _child_classes = dict(
        cell_function=cell_function_cls,
        auto_range=auto_range_cls,
        minimum=minimum_cls,
        maximum=maximum_cls,
        num_divisions=num_divisions_cls,
        all_zones=all_zones_cls,
        zones=zones_cls,
        axes=axes_cls,
        curves=curves_cls,
        print=print_cls,
        plot=plot_cls,
        write=write_cls,
    )

