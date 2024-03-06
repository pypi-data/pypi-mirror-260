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

from .surface import surface as surface_cls
class ungroup_surfaces(Command):
    """
    'ungroup_surfaces' command.
    
    Parameters
    ----------
        surface : str
            'surface' child.
    
    """

    fluent_name = "ungroup-surfaces"

    argument_names = \
        ['surface']

    _child_classes = dict(
        surface=surface_cls,
    )

