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

from .surfaces_5 import surfaces as surfaces_cls
from .name_3 import name as name_cls
class create_group_surfaces(Command):
    """
    'create_group_surfaces' command.
    
    Parameters
    ----------
        surfaces : typing.List[str]
            Select list of surfaces.
        name : str
            'name' child.
    
    """

    fluent_name = "create-group-surfaces"

    argument_names = \
        ['surfaces', 'name']

    _child_classes = dict(
        surfaces=surfaces_cls,
        name=name_cls,
    )

