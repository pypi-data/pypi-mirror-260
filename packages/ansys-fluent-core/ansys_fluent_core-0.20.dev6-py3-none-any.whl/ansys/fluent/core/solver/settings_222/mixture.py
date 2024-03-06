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

from .mixture_child import mixture_child

class mixture(NamedObject[mixture_child], _CreatableNamedObjectMixin[mixture_child]):
    """
    'mixture' child.
    """

    fluent_name = "mixture"

    child_object_type: mixture_child = mixture_child
    """
    child_object_type of mixture.
    """
