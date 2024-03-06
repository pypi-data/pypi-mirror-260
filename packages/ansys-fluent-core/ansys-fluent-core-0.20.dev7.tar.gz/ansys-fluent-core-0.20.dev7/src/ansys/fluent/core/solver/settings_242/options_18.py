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

from .print_6 import print as print_cls
from .plot_13 import plot as plot_cls
from .n_display_1 import n_display as n_display_cls
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['print', 'plot', 'n_display']

    _child_classes = dict(
        print=print_cls,
        plot=plot_cls,
        n_display=n_display_cls,
    )

