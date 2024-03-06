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

from .edc_pasr_mixing_model import edc_pasr_mixing_model as edc_pasr_mixing_model_cls
from .mixing_constant import mixing_constant as mixing_constant_cls
from .fractal_dimension import fractal_dimension as fractal_dimension_cls
class edc_pasr_model_options(Group):
    """
    'edc_pasr_model_options' child.
    """

    fluent_name = "edc-pasr-model-options"

    child_names = \
        ['edc_pasr_mixing_model', 'mixing_constant', 'fractal_dimension']

    _child_classes = dict(
        edc_pasr_mixing_model=edc_pasr_mixing_model_cls,
        mixing_constant=mixing_constant_cls,
        fractal_dimension=fractal_dimension_cls,
    )

