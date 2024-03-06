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
from .variable_2 import variable as variable_cls
class compute_sample(Command):
    """
    Compute minimum/maximum of a sample variable.
    
    Parameters
    ----------
        sample : str
            'sample' child.
        variable : str
            'variable' child.
    
    """

    fluent_name = "compute-sample"

    argument_names = \
        ['sample', 'variable']

    _child_classes = dict(
        sample=sample_cls,
        variable=variable_cls,
    )

