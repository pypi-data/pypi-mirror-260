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

from .archive_name import archive_name as archive_name_cls
class archive(Command):
    """
    Archive Project.
    
    Parameters
    ----------
        archive_name : str
            'archive_name' child.
    
    """

    fluent_name = "archive"

    argument_names = \
        ['archive_name']

    _child_classes = dict(
        archive_name=archive_name_cls,
    )

