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
from .surfaces import surfaces as surfaces_cls
from .techplot_scalars import techplot_scalars as techplot_scalars_cls
class dx(Command):
    """
    Write an IBM Data Explorer format file.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        surfaces : typing.List[str]
            Select surface.
        techplot_scalars : typing.List[str]
            'techplot_scalars' child.
    
    """

    fluent_name = "dx"

    argument_names = \
        ['file_name', 'surfaces', 'techplot_scalars']

    _child_classes = dict(
        file_name=file_name_cls,
        surfaces=surfaces_cls,
        techplot_scalars=techplot_scalars_cls,
    )

