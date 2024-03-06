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

from .file_name_1 import file_name as file_name_cls
from .zones import zones as zones_cls
class replace(Command):
    """
    Replace mesh and interpolate data.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        zones : bool
            'zones' child.
    
    """

    fluent_name = "replace"

    argument_names = \
        ['file_name', 'zones']

    _child_classes = dict(
        file_name=file_name_cls,
        zones=zones_cls,
    )

