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

from .blended_compressive_scheme import blended_compressive_scheme as blended_compressive_scheme_cls
from .pseudo_time_stabilization import pseudo_time_stabilization as pseudo_time_stabilization_cls
class additional_stabilization_controls(Group):
    """
    Additional advanced stability controls for VOF.
    """

    fluent_name = "additional-stabilization-controls"

    child_names = \
        ['blended_compressive_scheme', 'pseudo_time_stabilization']

    _child_classes = dict(
        blended_compressive_scheme=blended_compressive_scheme_cls,
        pseudo_time_stabilization=pseudo_time_stabilization_cls,
    )

