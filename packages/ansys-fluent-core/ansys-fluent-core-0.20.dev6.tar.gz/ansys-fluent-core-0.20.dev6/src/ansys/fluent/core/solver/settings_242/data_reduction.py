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

from .across_injections_enabled import across_injections_enabled as across_injections_enabled_cls
class data_reduction(Group):
    """
    'data_reduction' child.
    """

    fluent_name = "data-reduction"

    child_names = \
        ['across_injections_enabled']

    _child_classes = dict(
        across_injections_enabled=across_injections_enabled_cls,
    )

