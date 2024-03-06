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

from .convergence_reports_child import convergence_reports_child

class convergence_reports(NamedObject[convergence_reports_child], _CreatableNamedObjectMixin[convergence_reports_child]):
    """
    'convergence_reports' child.
    """

    fluent_name = "convergence-reports"

    child_object_type: convergence_reports_child = convergence_reports_child
    """
    child_object_type of convergence_reports.
    """
