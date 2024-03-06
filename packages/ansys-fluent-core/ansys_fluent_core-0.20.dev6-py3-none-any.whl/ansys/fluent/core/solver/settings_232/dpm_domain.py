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

from .option_6 import option as option_cls
from .partitioning_method_for_dpm_domain import partitioning_method_for_dpm_domain as partitioning_method_for_dpm_domain_cls
class dpm_domain(Group):
    """
    'dpm_domain' child.
    """

    fluent_name = "dpm-domain"

    child_names = \
        ['option', 'partitioning_method_for_dpm_domain']

    _child_classes = dict(
        option=option_cls,
        partitioning_method_for_dpm_domain=partitioning_method_for_dpm_domain_cls,
    )

