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

from .object_name_2 import object_name as object_name_cls
class display(Command):
    """
    Display cumulative-plot object.
    
    Parameters
    ----------
        object_name : str
            Object name.
    
    """

    fluent_name = "display"

    argument_names = \
        ['object_name']

    _child_classes = dict(
        object_name=object_name_cls,
    )

