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

from .flux_type import flux_type as flux_type_cls
class dbns_cases(Group):
    """
    'dbns_cases' child.
    """

    fluent_name = "dbns_cases"

    child_names = \
        ['flux_type']

    _child_classes = dict(
        flux_type=flux_type_cls,
    )

