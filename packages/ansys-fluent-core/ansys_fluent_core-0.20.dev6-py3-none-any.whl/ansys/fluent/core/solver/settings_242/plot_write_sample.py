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

from .plot_sample import plot_sample as plot_sample_cls
from .write_sample import write_sample as write_sample_cls
class plot_write_sample(Group):
    """
    'plot_write_sample' child.
    """

    fluent_name = "plot-write-sample"

    command_names = \
        ['plot_sample', 'write_sample']

    _child_classes = dict(
        plot_sample=plot_sample_cls,
        write_sample=write_sample_cls,
    )

