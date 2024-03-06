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

from .use_local_edge_length_factor import use_local_edge_length_factor as use_local_edge_length_factor_cls
from .gtol_length_factor import gtol_length_factor as gtol_length_factor_cls
from .gtol_absolute_value import gtol_absolute_value as gtol_absolute_value_cls
from .update import update as update_cls
class tolerance(Command):
    """
    Specification of mapped interface tolerance.
    
    Parameters
    ----------
        use_local_edge_length_factor : bool
            Enable tolerance based on local edge length factor instead of absolute tolerance.
        gtol_length_factor : real
            'gtol_length_factor' child.
        gtol_absolute_value : real
            'gtol_absolute_value' child.
        update : bool
            Update mapped interface with new tolerance.
    
    """

    fluent_name = "tolerance"

    argument_names = \
        ['use_local_edge_length_factor', 'gtol_length_factor',
         'gtol_absolute_value', 'update']

    _child_classes = dict(
        use_local_edge_length_factor=use_local_edge_length_factor_cls,
        gtol_length_factor=gtol_length_factor_cls,
        gtol_absolute_value=gtol_absolute_value_cls,
        update=update_cls,
    )

