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

from .window_name import window_name as window_name_cls
class set_window_by_name(Command):
    """
    Set a reserved graphics window to be the active window by its name.
    
    Parameters
    ----------
        window_name : str
            'window_name' child.
    
    """

    fluent_name = "set-window-by-name"

    argument_names = \
        ['window_name']

    _child_classes = dict(
        window_name=window_name_cls,
    )

