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

from .new import new as new_cls
from .open import open as open_cls
from .save import save as save_cls
from .save_as import save_as as save_as_cls
from .save_as_copy import save_as_copy as save_as_copy_cls
from .archive import archive as archive_cls
class parametric_project(Group):
    """
    'parametric_project' child.
    """

    fluent_name = "parametric-project"

    command_names = \
        ['new', 'open', 'save', 'save_as', 'save_as_copy', 'archive']

    _child_classes = dict(
        new=new_cls,
        open=open_cls,
        save=save_cls,
        save_as=save_as_cls,
        save_as_copy=save_as_copy_cls,
        archive=archive_cls,
    )

