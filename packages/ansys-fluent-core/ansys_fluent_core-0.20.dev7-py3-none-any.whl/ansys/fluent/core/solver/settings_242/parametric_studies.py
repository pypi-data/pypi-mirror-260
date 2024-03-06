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

from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .initialize_3 import initialize as initialize_cls
from .duplicate import duplicate as duplicate_cls
from .set_as_current import set_as_current as set_as_current_cls
from .use_base_data import use_base_data as use_base_data_cls
from .export_design_table import export_design_table as export_design_table_cls
from .import_design_table import import_design_table as import_design_table_cls
from .parametric_studies_child import parametric_studies_child

class parametric_studies(NamedObject[parametric_studies_child], _CreatableNamedObjectMixin[parametric_studies_child]):
    """
    'parametric_studies' child.
    """

    fluent_name = "parametric-studies"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy',
         'initialize', 'duplicate', 'set_as_current', 'use_base_data',
         'export_design_table', 'import_design_table']

    _child_classes = dict(
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        initialize=initialize_cls,
        duplicate=duplicate_cls,
        set_as_current=set_as_current_cls,
        use_base_data=use_base_data_cls,
        export_design_table=export_design_table_cls,
        import_design_table=import_design_table_cls,
    )

    child_object_type: parametric_studies_child = parametric_studies_child
    """
    child_object_type of parametric_studies.
    """
