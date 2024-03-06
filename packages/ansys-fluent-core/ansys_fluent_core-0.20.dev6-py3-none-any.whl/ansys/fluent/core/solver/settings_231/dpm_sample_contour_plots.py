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

from .select_sample import select_sample as select_sample_cls
from .plotting_grid_interval_size import plotting_grid_interval_size as plotting_grid_interval_size_cls
from .prepare_expressions import prepare_expressions as prepare_expressions_cls
class dpm_sample_contour_plots(Group):
    """
    'dpm_sample_contour_plots' child.
    """

    fluent_name = "dpm-sample-contour-plots"

    child_names = \
        ['select_sample', 'plotting_grid_interval_size']

    command_names = \
        ['prepare_expressions']

    _child_classes = dict(
        select_sample=select_sample_cls,
        plotting_grid_interval_size=plotting_grid_interval_size_cls,
        prepare_expressions=prepare_expressions_cls,
    )

