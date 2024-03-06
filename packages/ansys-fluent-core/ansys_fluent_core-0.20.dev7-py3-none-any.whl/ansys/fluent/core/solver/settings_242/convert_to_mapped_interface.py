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

from .convert_all import convert_all as convert_all_cls
from .convert_poorly_matching import convert_poorly_matching as convert_poorly_matching_cls
from .use_local_edge_length_factor import use_local_edge_length_factor as use_local_edge_length_factor_cls
from .gtol_length_factor import gtol_length_factor as gtol_length_factor_cls
from .gtol_absolute_value import gtol_absolute_value as gtol_absolute_value_cls
class convert_to_mapped_interface(Command):
    """
    Convert non-conformal mesh interface to mapped mesh interfaces.
    
    Parameters
    ----------
        convert_all : bool
            Convert all mesh interfaces to mapped mesh interfaces.
        convert_poorly_matching : bool
            Convert poorly matching mesh interfaces to mapped mesh interfaces.
        use_local_edge_length_factor : bool
            Enable tolerance based on local edge length factor instead of absolute tolerance.
        gtol_length_factor : real
            Tolerance.
        gtol_absolute_value : real
            Tolerance.
    
    """

    fluent_name = "convert-to-mapped-interface"

    argument_names = \
        ['convert_all', 'convert_poorly_matching',
         'use_local_edge_length_factor', 'gtol_length_factor',
         'gtol_absolute_value']

    _child_classes = dict(
        convert_all=convert_all_cls,
        convert_poorly_matching=convert_poorly_matching_cls,
        use_local_edge_length_factor=use_local_edge_length_factor_cls,
        gtol_length_factor=gtol_length_factor_cls,
        gtol_absolute_value=gtol_absolute_value_cls,
    )

