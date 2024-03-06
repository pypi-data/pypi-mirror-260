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

from .filename import filename as filename_cls
class read_views(Command):
    """
    Read views from a view file.
    
    Parameters
    ----------
        filename : str
            'filename' child.
    
    """

    fluent_name = "read-views"

    argument_names = \
        ['filename']

    _child_classes = dict(
        filename=filename_cls,
    )

