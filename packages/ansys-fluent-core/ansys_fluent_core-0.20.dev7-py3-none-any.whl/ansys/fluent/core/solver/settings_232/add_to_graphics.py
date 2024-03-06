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
class add_to_graphics(Command):
    """
    Add graphics object to existing graphics.
    
    Parameters
    ----------
        object_name : str
            'object_name' child.
    
    """

    fluent_name = "add-to-graphics"

    argument_names = \
        ['object_name']

    _child_classes = dict(
        object_name=object_name_cls,
    )

