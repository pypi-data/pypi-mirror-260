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

from .mapping_frequency import mapping_frequency as mapping_frequency_cls
from .under_relaxation_factor_1 import under_relaxation_factor as under_relaxation_factor_cls
class solution_controls(Command):
    """
    Specification of mapped frequency and under-relaxation factor for mapped interfaces.
    
    Parameters
    ----------
        mapping_frequency : int
            Mapping Frequency.
        under_relaxation_factor : real
            Under-Relaxation Factor.
    
    """

    fluent_name = "solution-controls"

    argument_names = \
        ['mapping_frequency', 'under_relaxation_factor']

    _child_classes = dict(
        mapping_frequency=mapping_frequency_cls,
        under_relaxation_factor=under_relaxation_factor_cls,
    )

