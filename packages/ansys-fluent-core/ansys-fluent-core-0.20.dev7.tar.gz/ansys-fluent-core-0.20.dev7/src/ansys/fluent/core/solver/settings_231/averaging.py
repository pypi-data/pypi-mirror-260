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

from .enable_node_based_averaging import enable_node_based_averaging as enable_node_based_averaging_cls
from .average_source_terms import average_source_terms as average_source_terms_cls
from .average_every_step import average_every_step as average_every_step_cls
from .averaging_kernel import averaging_kernel as averaging_kernel_cls
class averaging(Group):
    """
    Menu containing options to enable/disable node-based averaging of DPM variables and DPM source terms. 
    Please note that node-based averaging functionality is only available if source term linearization is not active.
    """

    fluent_name = "averaging"

    child_names = \
        ['enable_node_based_averaging', 'average_source_terms',
         'average_every_step', 'averaging_kernel']

    _child_classes = dict(
        enable_node_based_averaging=enable_node_based_averaging_cls,
        average_source_terms=average_source_terms_cls,
        average_every_step=average_every_step_cls,
        averaging_kernel=averaging_kernel_cls,
    )

