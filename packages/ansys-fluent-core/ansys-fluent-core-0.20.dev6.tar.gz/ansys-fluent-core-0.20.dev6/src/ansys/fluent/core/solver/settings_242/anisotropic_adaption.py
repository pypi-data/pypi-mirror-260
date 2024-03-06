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

from .operations import operations as operations_cls
from .iterations import iterations as iterations_cls
from .fixed_zones import fixed_zones as fixed_zones_cls
from .indicator import indicator as indicator_cls
from .target import target as target_cls
from .maximum_anisotropic_ratio import maximum_anisotropic_ratio as maximum_anisotropic_ratio_cls
from .minimum_edge_length_1 import minimum_edge_length as minimum_edge_length_cls
from .minimum_cell_quality_1 import minimum_cell_quality as minimum_cell_quality_cls
from .adapt_mesh_1 import adapt_mesh as adapt_mesh_cls
class anisotropic_adaption(Group):
    """
    Enter the anisotropic adaption menu.
    """

    fluent_name = "anisotropic-adaption"

    child_names = \
        ['operations', 'iterations', 'fixed_zones', 'indicator', 'target',
         'maximum_anisotropic_ratio', 'minimum_edge_length',
         'minimum_cell_quality']

    command_names = \
        ['adapt_mesh']

    _child_classes = dict(
        operations=operations_cls,
        iterations=iterations_cls,
        fixed_zones=fixed_zones_cls,
        indicator=indicator_cls,
        target=target_cls,
        maximum_anisotropic_ratio=maximum_anisotropic_ratio_cls,
        minimum_edge_length=minimum_edge_length_cls,
        minimum_cell_quality=minimum_cell_quality_cls,
        adapt_mesh=adapt_mesh_cls,
    )

