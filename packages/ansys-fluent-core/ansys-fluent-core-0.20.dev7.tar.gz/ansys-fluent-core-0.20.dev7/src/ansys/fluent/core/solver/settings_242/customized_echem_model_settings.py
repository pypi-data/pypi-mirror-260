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

from .memory_num_per_cell import memory_num_per_cell as memory_num_per_cell_cls
from .initial_soc_2 import initial_soc as initial_soc_cls
from .reference_capacity import reference_capacity as reference_capacity_cls
class customized_echem_model_settings(Group):
    """
    User-defined echem model.
    """

    fluent_name = "customized-echem-model-settings"

    child_names = \
        ['memory_num_per_cell', 'initial_soc', 'reference_capacity']

    _child_classes = dict(
        memory_num_per_cell=memory_num_per_cell_cls,
        initial_soc=initial_soc_cls,
        reference_capacity=reference_capacity_cls,
    )

