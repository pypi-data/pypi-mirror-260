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

from .child_object_type_child import child_object_type_child

class ablation_species_mf(NamedObject[child_object_type_child], _CreatableNamedObjectMixin[child_object_type_child]):
    """
    'ablation_species_mf' child.
    """

    fluent_name = "ablation-species-mf"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of ablation_species_mf.
    """
