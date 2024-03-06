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
from .clear_repeats import clear_repeats as clear_repeats_cls
from .periodic_instancing_child import periodic_instancing_child

class periodic_instancing(NamedObject[periodic_instancing_child], _CreatableNamedObjectMixin[periodic_instancing_child]):
    """
    Create/edit/del periodic instancing.
    """

    fluent_name = "periodic-instancing"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy',
         'clear_repeats']

    _child_classes = dict(
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        clear_repeats=clear_repeats_cls,
    )

    child_object_type: periodic_instancing_child = periodic_instancing_child
    """
    child_object_type of periodic_instancing.
    """
