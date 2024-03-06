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
from .cell_func_domain_export import cell_func_domain_export as cell_func_domain_export_cls
class ensight_gold(Command):
    """
    Write EnSight Gold geometry, velocity, and scalar files.
    
    Parameters
    ----------
        name : str
            'name' child.
        cell_func_domain_export : typing.List[str]
            'cell_func_domain_export' child.
    
    """

    fluent_name = "ensight-gold"

    argument_names = \
        ['name', 'cell_func_domain_export']

    _child_classes = dict(
        name=name_cls,
        cell_func_domain_export=cell_func_domain_export_cls,
    )

