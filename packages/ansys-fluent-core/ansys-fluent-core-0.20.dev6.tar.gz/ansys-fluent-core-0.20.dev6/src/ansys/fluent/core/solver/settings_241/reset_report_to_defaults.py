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

from .report_name import report_name as report_name_cls
class reset_report_to_defaults(Command):
    """
    Reset all report settings to default for the provided simulation report.
    
    Parameters
    ----------
        report_name : str
            'report_name' child.
    
    """

    fluent_name = "reset-report-to-defaults"

    argument_names = \
        ['report_name']

    _child_classes = dict(
        report_name=report_name_cls,
    )

