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

from .object_at import object_at as object_at_cls
class list_properties(Command):
    """
    List properties of selected object.
    
    Parameters
    ----------
        object_at : int
            Select object index to delete.
    
    """

    fluent_name = "list-properties"

    argument_names = \
        ['object_at']

    _child_classes = dict(
        object_at=object_at_cls,
    )

