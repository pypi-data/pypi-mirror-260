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
from .cellzones_1 import cellzones as cellzones_cls
class stack_modify_fcu(Command):
    """
    Modify stack units.
    
    Parameters
    ----------
        fcu_name : str
            'fcu_name' child.
        cellzones : typing.List[str]
            Enter cell zone name list.
    
    """

    fluent_name = "stack-modify-fcu"

    argument_names = \
        ['fcu_name', 'cellzones']

    _child_classes = dict(
        fcu_name=fcu_name_cls,
        cellzones=cellzones_cls,
    )

