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

from .database_type import database_type as database_type_cls
from .copy_by_formula import copy_by_formula as copy_by_formula_cls
from .copy_by_name import copy_by_name as copy_by_name_cls
from .list_materials import list_materials as list_materials_cls
from .list_properties import list_properties as list_properties_cls
class database(Group):
    """
    'database' child.
    """

    fluent_name = "database"

    child_names = \
        ['database_type']

    command_names = \
        ['copy_by_formula', 'copy_by_name', 'list_materials',
         'list_properties']

    _child_classes = dict(
        database_type=database_type_cls,
        copy_by_formula=copy_by_formula_cls,
        copy_by_name=copy_by_name_cls,
        list_materials=list_materials_cls,
        list_properties=list_properties_cls,
    )

