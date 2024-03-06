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

from .fcu_name import fcu_name as fcu_name_cls
class stack_delete_fcu(Command):
    """
    Delete stack units.
    
    Parameters
    ----------
        fcu_name : str
            'fcu_name' child.
    
    """

    fluent_name = "stack-delete-fcu"

    argument_names = \
        ['fcu_name']

    _child_classes = dict(
        fcu_name=fcu_name_cls,
    )

