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

from .keep_linearized_source_terms_constant import keep_linearized_source_terms_constant as keep_linearized_source_terms_constant_cls
from .linearize_source_terms import linearize_source_terms as linearize_source_terms_cls
from .linearized_source_terms_limiter import linearized_source_terms_limiter as linearized_source_terms_limiter_cls
class linearization(Group):
    """
    Menu containing options to enable/disable linearization of DPM source terms. 
    Please note that source term linearization is only available if the node-based averaging option is not active.
    """

    fluent_name = "linearization"

    child_names = \
        ['keep_linearized_source_terms_constant', 'linearize_source_terms',
         'linearized_source_terms_limiter']

    _child_classes = dict(
        keep_linearized_source_terms_constant=keep_linearized_source_terms_constant_cls,
        linearize_source_terms=linearize_source_terms_cls,
        linearized_source_terms_limiter=linearized_source_terms_limiter_cls,
    )

