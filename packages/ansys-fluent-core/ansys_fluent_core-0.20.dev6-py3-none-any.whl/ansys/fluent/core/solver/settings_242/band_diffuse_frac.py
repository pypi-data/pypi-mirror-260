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
from .band_diffuse_frac_child import band_diffuse_frac_child

class band_diffuse_frac(NamedObject[band_diffuse_frac_child], _NonCreatableNamedObjectMixin[band_diffuse_frac_child]):
    """
    Specify diffuse fraction.
    """

    fluent_name = "band-diffuse-frac"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy']

    _child_classes = dict(
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
    )

    child_object_type: band_diffuse_frac_child = band_diffuse_frac_child
    """
    child_object_type of band_diffuse_frac.
    """
