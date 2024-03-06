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

from .type_1 import type as type_cls
from .formula import formula as formula_cls
class copy_database_material_by_formula(Command):
    """
    'copy_database_material_by_formula' command.
    
    Parameters
    ----------
        type : str
            'type' child.
        formula : str
            'formula' child.
    
    """

    fluent_name = "copy-database-material-by-formula"

    argument_names = \
        ['type', 'formula']

    _child_classes = dict(
        type=type_cls,
        formula=formula_cls,
    )

