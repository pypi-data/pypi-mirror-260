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

from .initialize import initialize as initialize_cls
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
        ['initialize', 'duplicate', 'set_as_current', 'use_base_data',
         'export_design_table', 'import_design_table']

    _child_classes = dict(
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
