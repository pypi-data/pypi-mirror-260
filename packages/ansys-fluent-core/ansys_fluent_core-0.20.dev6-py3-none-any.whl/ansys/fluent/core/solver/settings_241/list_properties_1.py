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

from .object_name import object_name as object_name_cls
class list_properties(Command):
    """
    List active properties of the object.
    
    Parameters
    ----------
        object_name : str
            Select object for which properties are to be listed.
    
    """

    fluent_name = "list-properties"

    argument_names = \
        ['object_name']

    _child_classes = dict(
        object_name=object_name_cls,
    )

