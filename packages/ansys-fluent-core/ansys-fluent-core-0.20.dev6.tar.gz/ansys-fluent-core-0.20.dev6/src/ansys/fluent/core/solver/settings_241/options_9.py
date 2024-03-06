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

from .criterion_type import criterion_type as criterion_type_cls
from .n_save import n_save as n_save_cls
from .normalize import normalize as normalize_cls
from .n_maximize_norms import n_maximize_norms as n_maximize_norms_cls
from .enhanced_continuity_residual import enhanced_continuity_residual as enhanced_continuity_residual_cls
from .residual_values import residual_values as residual_values_cls
from .print_2 import print as print_cls
from .plot import plot as plot_cls
from .n_display import n_display as n_display_cls
class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['criterion_type', 'n_save', 'normalize', 'n_maximize_norms',
         'enhanced_continuity_residual', 'residual_values', 'print', 'plot',
         'n_display']

    _child_classes = dict(
        criterion_type=criterion_type_cls,
        n_save=n_save_cls,
        normalize=normalize_cls,
        n_maximize_norms=n_maximize_norms_cls,
        enhanced_continuity_residual=enhanced_continuity_residual_cls,
        residual_values=residual_values_cls,
        print=print_cls,
        plot=plot_cls,
        n_display=n_display_cls,
    )

