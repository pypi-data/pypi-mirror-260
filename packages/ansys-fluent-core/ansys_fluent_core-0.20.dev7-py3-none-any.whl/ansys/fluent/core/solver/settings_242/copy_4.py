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

from .from_name import from_name as from_name_cls
from .new_name import new_name as new_name_cls
class copy(Command):
    """
    Copy graphics object.
    
    Parameters
    ----------
        from_name : str
            'from_name' child.
        new_name : str
            'new_name' child.
    
    """

    fluent_name = "copy"

    argument_names = \
        ['from_name', 'new_name']

    _child_classes = dict(
        from_name=from_name_cls,
        new_name=new_name_cls,
    )

