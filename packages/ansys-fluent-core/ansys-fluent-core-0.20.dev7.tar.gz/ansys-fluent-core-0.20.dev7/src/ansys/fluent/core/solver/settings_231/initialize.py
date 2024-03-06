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

from .init_type import init_type as init_type_cls
class initialize(Command):
    """
    'initialize' command.
    
    Parameters
    ----------
        init_type : str
            'init_type' child.
    
    """

    fluent_name = "initialize"

    argument_names = \
        ['init_type']

    _child_classes = dict(
        init_type=init_type_cls,
    )

