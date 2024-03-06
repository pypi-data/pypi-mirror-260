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

from .min_diam import min_diam as min_diam_cls
from .max_diam import max_diam as max_diam_cls
from .mean_diam import mean_diam as mean_diam_cls
from .spread import spread as spread_cls
from .number_of_diameters import number_of_diameters as number_of_diameters_cls
class rosin_rammler_settings(Group):
    """
    'rosin_rammler_settings' child.
    """

    fluent_name = "rosin-rammler-settings"

    child_names = \
        ['min_diam', 'max_diam', 'mean_diam', 'spread', 'number_of_diameters']

    _child_classes = dict(
        min_diam=min_diam_cls,
        max_diam=max_diam_cls,
        mean_diam=mean_diam_cls,
        spread=spread_cls,
        number_of_diameters=number_of_diameters_cls,
    )

