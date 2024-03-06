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
from .report_definition import report_definition as report_definition_cls
class report_definitions_child(Group):
    """
    'child_object_type' of report_definitions.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'report_definition']

    _child_classes = dict(
        name=name_cls,
        report_definition=report_definition_cls,
    )

