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

from .filename_5 import filename as filename_cls
from .capacity import capacity as capacity_cls
from .number_dod_level import number_dod_level as number_dod_level_cls
from .min_dod import min_dod as min_dod_cls
from .max_dod import max_dod as max_dod_cls
from .capacity_fade_enabled import capacity_fade_enabled as capacity_fade_enabled_cls
class ntgk_curve_fitting(Command):
    """
    NTGK parameter estimation tool.
    
    Parameters
    ----------
        filename : typing.List[str]
            File names used in the NTGK model fitting.
        capacity : real
            Battery capacity used in the NTGK model fitting.
        number_dod_level : int
            Number of DOD-levels used in the NTGK model fitting.
        min_dod : real
            Minimum DOD used in the NTGK model fitting.
        max_dod : real
            Maximum DOD used in the NTGK model fitting.
        capacity_fade_enabled : bool
            Include Capacity Fade Effect in the NTGK model fitting.
    
    """

    fluent_name = "ntgk-curve-fitting"

    argument_names = \
        ['filename', 'capacity', 'number_dod_level', 'min_dod', 'max_dod',
         'capacity_fade_enabled']

    _child_classes = dict(
        filename=filename_cls,
        capacity=capacity_cls,
        number_dod_level=number_dod_level_cls,
        min_dod=min_dod_cls,
        max_dod=max_dod_cls,
        capacity_fade_enabled=capacity_fade_enabled_cls,
    )

