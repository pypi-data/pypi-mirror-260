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
from .neutral_involved_interaction import neutral_involved_interaction as neutral_involved_interaction_cls
from .charged_particle_interaction import charged_particle_interaction as charged_particle_interaction_cls
class child_object_type_child(Group):
    """
    'child_object_type' of child_object_type.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['option', 'neutral_involved_interaction',
         'charged_particle_interaction']

    _child_classes = dict(
        option=option_cls,
        neutral_involved_interaction=neutral_involved_interaction_cls,
        charged_particle_interaction=charged_particle_interaction_cls,
    )

