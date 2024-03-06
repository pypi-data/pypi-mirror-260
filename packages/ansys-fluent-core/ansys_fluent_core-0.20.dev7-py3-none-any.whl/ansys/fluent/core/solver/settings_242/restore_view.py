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

from .view_name import view_name as view_name_cls
class restore_view(Command):
    """
    Use a saved view.
    
    Parameters
    ----------
        view_name : str
            'view_name' child.
    
    """

    fluent_name = "restore-view"

    argument_names = \
        ['view_name']

    _child_classes = dict(
        view_name=view_name_cls,
    )

