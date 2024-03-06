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

from .register_name import register_name as register_name_cls
class list_properties(Command):
    """
    List the properties of a definition for poor mesh numerics.
    
    Parameters
    ----------
        register_name : str
            'register_name' child.
    
    """

    fluent_name = "list-properties"

    argument_names = \
        ['register_name']

    _child_classes = dict(
        register_name=register_name_cls,
    )

