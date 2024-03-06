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

from .names import names as names_cls
class compute(Command):
    """
    'compute' command.
    
    Parameters
    ----------
        names : typing.List[str]
            'names' child.
    
    """

    fluent_name = "compute"

    argument_names = \
        ['names']

    _child_classes = dict(
        names=names_cls,
    )

