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

from .macro_filename import macro_filename as macro_filename_cls
class execute_macro(Command):
    """
    Run a previously defined macro.
    
    Parameters
    ----------
        macro_filename : str
            'macro_filename' child.
    
    """

    fluent_name = "execute-macro"

    argument_names = \
        ['macro_filename']

    _child_classes = dict(
        macro_filename=macro_filename_cls,
    )

