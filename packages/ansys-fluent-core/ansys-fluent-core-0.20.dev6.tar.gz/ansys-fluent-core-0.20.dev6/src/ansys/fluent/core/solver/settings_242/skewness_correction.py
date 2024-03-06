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

from .limit_pressure_correction_gradient import limit_pressure_correction_gradient as limit_pressure_correction_gradient_cls
class skewness_correction(Group):
    """
    Skewness correction related stabiity controls for multiphase flow.
    """

    fluent_name = "skewness-correction"

    child_names = \
        ['limit_pressure_correction_gradient']

    _child_classes = dict(
        limit_pressure_correction_gradient=limit_pressure_correction_gradient_cls,
    )

