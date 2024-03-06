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

from .print_level import print_level as print_level_cls
class mesh_info(Command):
    """
    Print zone information size.
    
    Parameters
    ----------
        print_level : int
            Print zone information size.
    
    """

    fluent_name = "mesh-info"

    argument_names = \
        ['print_level']

    _child_classes = dict(
        print_level=print_level_cls,
    )

