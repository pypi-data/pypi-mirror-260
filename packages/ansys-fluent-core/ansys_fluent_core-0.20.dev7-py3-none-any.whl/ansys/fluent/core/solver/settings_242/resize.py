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

from .size import size as size_cls
class resize(CommandWithPositionalArgs):
    """
    Set number of objects for list-object.
    
    Parameters
    ----------
        size : int
            New size for list-object.
    
    """

    fluent_name = "resize"

    argument_names = \
        ['size']

    _child_classes = dict(
        size=size_cls,
    )

