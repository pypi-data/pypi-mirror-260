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

from .key_1 import key as key_cls
class delete_keyframe(Command):
    """
    Delete a keyframe.
    
    Parameters
    ----------
        key : int
            'key' child.
    
    """

    fluent_name = "delete-keyframe"

    argument_names = \
        ['key']

    _child_classes = dict(
        key=key_cls,
    )

