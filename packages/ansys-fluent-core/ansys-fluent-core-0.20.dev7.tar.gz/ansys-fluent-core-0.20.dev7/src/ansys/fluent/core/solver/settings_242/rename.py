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

from .new_1 import new as new_cls
from .old import old as old_cls
class rename(CommandWithPositionalArgs):
    """
    Rename the object.
    
    Parameters
    ----------
        new : str
            New name for the object.
        old : str
            Select object to rename.
    
    """

    fluent_name = "rename"

    argument_names = \
        ['new', 'old']

    _child_classes = dict(
        new=new_cls,
        old=old_cls,
    )

