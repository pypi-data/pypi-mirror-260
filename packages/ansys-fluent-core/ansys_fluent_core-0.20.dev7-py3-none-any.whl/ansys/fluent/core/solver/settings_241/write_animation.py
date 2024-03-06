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

from .format_name import format_name as format_name_cls
class write_animation(Command):
    """
    Write animation sequence to the file.
    
    Parameters
    ----------
        format_name : str
            'format_name' child.
    
    """

    fluent_name = "write-animation"

    argument_names = \
        ['format_name']

    _child_classes = dict(
        format_name=format_name_cls,
    )

