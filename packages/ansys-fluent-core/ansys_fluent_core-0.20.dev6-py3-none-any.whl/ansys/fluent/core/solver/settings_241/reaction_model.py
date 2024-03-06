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
class reaction_model(Group):
    """
    'reaction_model' child.
    """

    fluent_name = "reaction-model"

    child_names = \
        ['option']

    _child_classes = dict(
        option=option_cls,
    )

