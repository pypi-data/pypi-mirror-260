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

from .roughness_correlation import roughness_correlation as roughness_correlation_cls
class transition_sst_options(Group):
    """
    'transition_sst_options' child.
    """

    fluent_name = "transition-sst-options"

    child_names = \
        ['roughness_correlation']

    _child_classes = dict(
        roughness_correlation=roughness_correlation_cls,
    )

