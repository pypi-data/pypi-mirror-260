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

from .enable_9 import enable as enable_cls
from .beams import beams as beams_cls
from .statistics import statistics as statistics_cls
from .sampling_iterations import sampling_iterations as sampling_iterations_cls
from .index_of_refraction import index_of_refraction as index_of_refraction_cls
from .report import report as report_cls
from .verbosity_2 import verbosity as verbosity_cls
class optics(Group):
    """
    Enter the optics model menu.
    """

    fluent_name = "optics"

    child_names = \
        ['enable', 'beams', 'statistics', 'sampling_iterations',
         'index_of_refraction', 'report', 'verbosity']

    _child_classes = dict(
        enable=enable_cls,
        beams=beams_cls,
        statistics=statistics_cls,
        sampling_iterations=sampling_iterations_cls,
        index_of_refraction=index_of_refraction_cls,
        report=report_cls,
        verbosity=verbosity_cls,
    )

