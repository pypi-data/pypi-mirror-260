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

from .playback import playback as playback_cls
class animations(Group):
    """
    'animations' child.
    """

    fluent_name = "animations"

    child_names = \
        ['playback']

    _child_classes = dict(
        playback=playback_cls,
    )

