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

from .dpm_domain import dpm_domain as dpm_domain_cls
from .ordered_accumulation import ordered_accumulation as ordered_accumulation_cls
class hybrid_options(Group):
    """
    'hybrid_options' child.
    """

    fluent_name = "hybrid-options"

    child_names = \
        ['dpm_domain', 'ordered_accumulation']

    _child_classes = dict(
        dpm_domain=dpm_domain_cls,
        ordered_accumulation=ordered_accumulation_cls,
    )

