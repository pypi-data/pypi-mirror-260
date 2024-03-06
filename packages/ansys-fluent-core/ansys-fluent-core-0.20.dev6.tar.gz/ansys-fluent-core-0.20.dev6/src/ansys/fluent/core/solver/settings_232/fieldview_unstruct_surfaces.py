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

from .options import options as options_cls
from .name import name as name_cls
from .surfaces import surfaces as surfaces_cls
from .cell_func_domain import cell_func_domain as cell_func_domain_cls
class fieldview_unstruct_surfaces(Command):
    """
    Write a Fieldview unstructured surface mesh, data.
    
    Parameters
    ----------
        options : str
            'options' child.
        name : str
            'name' child.
        surfaces : typing.List[str]
            'surfaces' child.
        cell_func_domain : typing.List[str]
            'cell_func_domain' child.
    
    """

    fluent_name = "fieldview-unstruct-surfaces"

    argument_names = \
        ['options', 'name', 'surfaces', 'cell_func_domain']

    _child_classes = dict(
        options=options_cls,
        name=name_cls,
        surfaces=surfaces_cls,
        cell_func_domain=cell_func_domain_cls,
    )

