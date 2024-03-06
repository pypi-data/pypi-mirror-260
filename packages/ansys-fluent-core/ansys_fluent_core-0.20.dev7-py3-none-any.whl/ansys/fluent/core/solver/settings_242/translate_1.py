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

from .offset import offset as offset_cls
class translate(Command):
    """
    Translate the mesh.
    
    Parameters
    ----------
        offset : typing.List[real]
            'offset' child.
    
    """

    fluent_name = "translate"

    argument_names = \
        ['offset']

    _child_classes = dict(
        offset=offset_cls,
    )

