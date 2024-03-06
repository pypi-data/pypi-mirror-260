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
from .pseudo_transient_stabilization import pseudo_transient_stabilization as pseudo_transient_stabilization_cls
class additional_stabilization_controls(Group):
    """
    'additional_stabilization_controls' child.
    """

    fluent_name = "additional-stabilization-controls"

    child_names = \
        ['blended_compressive_scheme', 'pseudo_transient_stabilization']

    _child_classes = dict(
        blended_compressive_scheme=blended_compressive_scheme_cls,
        pseudo_transient_stabilization=pseudo_transient_stabilization_cls,
    )

