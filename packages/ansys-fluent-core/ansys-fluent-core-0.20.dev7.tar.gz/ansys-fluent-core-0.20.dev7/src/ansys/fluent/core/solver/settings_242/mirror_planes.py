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
from .create_3 import create as create_cls
from .mirror_planes_child import mirror_planes_child

class mirror_planes(NamedObject[mirror_planes_child], _NonCreatableNamedObjectMixin[mirror_planes_child]):
    """
    Enter the mirror planes options menu.
    """

    fluent_name = "mirror-planes"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy',
         'create']

    _child_classes = dict(
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        create=create_cls,
    )

    child_object_type: mirror_planes_child = mirror_planes_child
    """
    child_object_type of mirror_planes.
    """
