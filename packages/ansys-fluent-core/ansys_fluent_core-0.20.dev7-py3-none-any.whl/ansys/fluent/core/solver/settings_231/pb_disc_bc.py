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

from .turb_visc_func_mf_child import turb_visc_func_mf_child

class pb_disc_bc(NamedObject[turb_visc_func_mf_child], _NonCreatableNamedObjectMixin[turb_visc_func_mf_child]):
    """
    'pb_disc_bc' child.
    """

    fluent_name = "pb-disc-bc"

    child_object_type: turb_visc_func_mf_child = turb_visc_func_mf_child
    """
    child_object_type of pb_disc_bc.
    """
