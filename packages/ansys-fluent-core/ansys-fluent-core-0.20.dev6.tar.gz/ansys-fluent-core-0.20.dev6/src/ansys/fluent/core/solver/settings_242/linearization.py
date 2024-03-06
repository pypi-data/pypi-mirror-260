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

from .constant_during_flow_iterations import constant_during_flow_iterations as constant_during_flow_iterations_cls
from .enabled_3 import enabled as enabled_cls
from .enhanced_form_enabled import enhanced_form_enabled as enhanced_form_enabled_cls
from .limiter import limiter as limiter_cls
class linearization(Group):
    """
    Menu containing options to enable/disable linearization of DPM source terms. 
    Please note that source term linearization is only available if the node-based averaging option is not active.
    """

    fluent_name = "linearization"

    child_names = \
        ['constant_during_flow_iterations', 'enabled',
         'enhanced_form_enabled', 'limiter']

    _child_classes = dict(
        constant_during_flow_iterations=constant_during_flow_iterations_cls,
        enabled=enabled_cls,
        enhanced_form_enabled=enhanced_form_enabled_cls,
        limiter=limiter_cls,
    )

