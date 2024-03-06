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

from .filepath import filepath as filepath_cls
from .delete_existing import delete_existing as delete_existing_cls
class import_design_table(Command):
    """
    Import Design Point Table.
    
    Parameters
    ----------
        filepath : str
            'filepath' child.
        delete_existing : bool
            'delete_existing' child.
    
    """

    fluent_name = "import-design-table"

    argument_names = \
        ['filepath', 'delete_existing']

    _child_classes = dict(
        filepath=filepath_cls,
        delete_existing=delete_existing_cls,
    )

