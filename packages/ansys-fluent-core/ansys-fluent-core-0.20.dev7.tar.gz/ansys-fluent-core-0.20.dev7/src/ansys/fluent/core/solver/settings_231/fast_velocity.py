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

from .name import name as name_cls
class fast_velocity(Command):
    """
    Write a FAST/Plot3D unstructured vector function file.
    
    Parameters
    ----------
        name : str
            'name' child.
    
    """

    fluent_name = "fast-velocity"

    argument_names = \
        ['name']

    _child_classes = dict(
        name=name_cls,
    )

