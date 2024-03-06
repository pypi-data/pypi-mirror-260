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

from .surfaces_4 import surfaces as surfaces_cls
from .graphics import graphics as graphics_cls
from .plot_2 import plot as plot_cls
from .scene import scene as scene_cls
from .animations import animations as animations_cls
from .report_1 import report as report_cls
class results(Group):
    """
    'results' child.
    """

    fluent_name = "results"

    child_names = \
        ['surfaces', 'graphics', 'plot', 'scene', 'animations', 'report']

    _child_classes = dict(
        surfaces=surfaces_cls,
        graphics=graphics_cls,
        plot=plot_cls,
        scene=scene_cls,
        animations=animations_cls,
        report=report_cls,
    )

