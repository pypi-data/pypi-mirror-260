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

from .sample import sample as sample_cls
class delete_sample(Command):
    """
    'delete_sample' command.
    
    Parameters
    ----------
        sample : str
            'sample' child.
    
    """

    fluent_name = "delete-sample"

    argument_names = \
        ['sample']

    _child_classes = dict(
        sample=sample_cls,
    )

