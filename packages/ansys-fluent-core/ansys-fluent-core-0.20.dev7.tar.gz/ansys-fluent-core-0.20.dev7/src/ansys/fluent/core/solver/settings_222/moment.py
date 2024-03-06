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

from .moment_child import moment_child

class moment(NamedObject[moment_child], _CreatableNamedObjectMixin[moment_child]):
    """
    'moment' child.
    """

    fluent_name = "moment"

    child_object_type: moment_child = moment_child
    """
    child_object_type of moment.
    """
