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

from .delete_1 import delete as delete_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .display_5 import display as display_cls
from .cumulative_plot_child import cumulative_plot_child

class cumulative_plot(NamedObject[cumulative_plot_child], _CreatableNamedObjectMixin[cumulative_plot_child]):
    """
    Cumulative plots.
    """

    fluent_name = "cumulative-plot"

    command_names = \
        ['delete', 'list', 'list_properties', 'make_a_copy', 'display']

    _child_classes = dict(
        delete=delete_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        display=display_cls,
    )

    child_object_type: cumulative_plot_child = cumulative_plot_child
    """
    child_object_type of cumulative_plot.
    """
