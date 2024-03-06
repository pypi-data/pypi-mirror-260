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

from .name_2 import name as name_cls
class remove_dataset(Command):
    """
    Remove dataset.
    
    Parameters
    ----------
        name : str
            'name' child.
    
    """

    fluent_name = "remove-dataset"

    argument_names = \
        ['name']

    _child_classes = dict(
        name=name_cls,
    )

