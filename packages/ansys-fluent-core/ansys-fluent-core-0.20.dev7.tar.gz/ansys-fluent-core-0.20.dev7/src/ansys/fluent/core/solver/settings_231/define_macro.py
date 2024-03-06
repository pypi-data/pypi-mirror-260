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
class define_macro(Command):
    """
    Save input to a named macro.
    
    Parameters
    ----------
        filename : str
            'filename' child.
    
    """

    fluent_name = "define-macro"

    argument_names = \
        ['filename']

    _child_classes = dict(
        filename=filename_cls,
    )

