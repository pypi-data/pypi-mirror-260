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

from .controls import controls as controls_cls
from .methods_1 import methods as methods_cls
from .report_definitions import report_definitions as report_definitions_cls
from .initialization import initialization as initialization_cls
from .run_calculation import run_calculation as run_calculation_cls
class solution(Group):
    """
    'solution' child.
    """

    fluent_name = "solution"

    child_names = \
        ['controls', 'methods', 'report_definitions', 'initialization',
         'run_calculation']

    _child_classes = dict(
        controls=controls_cls,
        methods=methods_cls,
        report_definitions=report_definitions_cls,
        initialization=initialization_cls,
        run_calculation=run_calculation_cls,
    )

