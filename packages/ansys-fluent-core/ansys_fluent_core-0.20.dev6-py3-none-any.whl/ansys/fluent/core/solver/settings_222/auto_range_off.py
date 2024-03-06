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

from .clip_to_range import clip_to_range as clip_to_range_cls
from .minimum import minimum as minimum_cls
from .maximum import maximum as maximum_cls
class auto_range_off(Group):
    """
    'auto_range_off' child.
    """

    fluent_name = "auto-range-off"

    child_names = \
        ['clip_to_range', 'minimum', 'maximum']

    _child_classes = dict(
        clip_to_range=clip_to_range_cls,
        minimum=minimum_cls,
        maximum=maximum_cls,
    )

