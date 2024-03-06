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

from .ni import ni as ni_cls
from .nj import nj as nj_cls
from .nk import nk as nk_cls
from .xe import xe as xe_cls
from .len import len as len_cls
class beach_dir_list_child(Group):
    """
    'child_object_type' of beach_dir_list.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['ni', 'nj', 'nk', 'xe', 'len']

    _child_classes = dict(
        ni=ni_cls,
        nj=nj_cls,
        nk=nk_cls,
        xe=xe_cls,
        len=len_cls,
    )

