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

from .option_7 import option as option_cls
class reaction_mechs(Group):
    """
    'reaction_mechs' child.
    """

    fluent_name = "reaction-mechs"

    child_names = \
        ['option']

    _child_classes = dict(
        option=option_cls,
    )

