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

from .animation_file_name import animation_file_name as animation_file_name_cls
class read_animation_file(Command):
    """
    Read new animation from file or already-defined animations.
    
    Parameters
    ----------
        animation_file_name : str
            'animation_file_name' child.
    
    """

    fluent_name = "read-animation-file"

    argument_names = \
        ['animation_file_name']

    _child_classes = dict(
        animation_file_name=animation_file_name_cls,
    )

