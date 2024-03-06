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

from .change_curr_sample import change_curr_sample as change_curr_sample_cls
from .sample import sample as sample_cls
class weighting_variable(Command):
    """
    Choose the weighting variable for the averaging in each bin in the data reduction.
    
    Parameters
    ----------
        change_curr_sample : bool
            'change_curr_sample' child.
        sample : str
            'sample' child.
    
    """

    fluent_name = "weighting-variable"

    argument_names = \
        ['change_curr_sample', 'sample']

    _child_classes = dict(
        change_curr_sample=change_curr_sample_cls,
        sample=sample_cls,
    )

