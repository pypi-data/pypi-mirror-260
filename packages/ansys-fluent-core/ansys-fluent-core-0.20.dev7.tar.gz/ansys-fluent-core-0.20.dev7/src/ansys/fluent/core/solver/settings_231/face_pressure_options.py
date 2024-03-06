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

from .pressure_corr_grad import pressure_corr_grad as pressure_corr_grad_cls
from .face_pressure_calculation_method import face_pressure_calculation_method as face_pressure_calculation_method_cls
from .exclude_transient_term_in_face_pressure_calc import exclude_transient_term_in_face_pressure_calc as exclude_transient_term_in_face_pressure_calc_cls
class face_pressure_options(Group):
    """
    Set face pressure options.
    """

    fluent_name = "face-pressure-options"

    child_names = \
        ['pressure_corr_grad', 'face_pressure_calculation_method',
         'exclude_transient_term_in_face_pressure_calc']

    _child_classes = dict(
        pressure_corr_grad=pressure_corr_grad_cls,
        face_pressure_calculation_method=face_pressure_calculation_method_cls,
        exclude_transient_term_in_face_pressure_calc=exclude_transient_term_in_face_pressure_calc_cls,
    )

