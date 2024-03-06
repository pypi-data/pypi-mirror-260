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

from .mg_controls import mg_controls as mg_controls_cls
from .amg_controls import amg_controls as amg_controls_cls
from .fas_mg_controls import fas_mg_controls as fas_mg_controls_cls
from .amg_gpgpu_options import amg_gpgpu_options as amg_gpgpu_options_cls
class multi_grid(Group):
    """
    'multi_grid' child.
    """

    fluent_name = "multi-grid"

    child_names = \
        ['mg_controls', 'amg_controls', 'fas_mg_controls',
         'amg_gpgpu_options']

    _child_classes = dict(
        mg_controls=mg_controls_cls,
        amg_controls=amg_controls_cls,
        fas_mg_controls=fas_mg_controls_cls,
        amg_gpgpu_options=amg_gpgpu_options_cls,
    )

