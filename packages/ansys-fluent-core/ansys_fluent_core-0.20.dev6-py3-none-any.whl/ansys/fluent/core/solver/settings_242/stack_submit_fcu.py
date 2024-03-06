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

from .submit import submit as submit_cls
class stack_submit_fcu(Command):
    """
    Apply stack units settings.
    
    Parameters
    ----------
        submit : bool
            'submit' child.
    
    """

    fluent_name = "stack-submit-fcu"

    argument_names = \
        ['submit']

    _child_classes = dict(
        submit=submit_cls,
    )

