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

from .gradient_based import gradient_based as gradient_based_cls
class design(Group):
    """
    'design' child.
    """

    fluent_name = "design"

    child_names = \
        ['gradient_based']

    _child_classes = dict(
        gradient_based=gradient_based_cls,
    )

