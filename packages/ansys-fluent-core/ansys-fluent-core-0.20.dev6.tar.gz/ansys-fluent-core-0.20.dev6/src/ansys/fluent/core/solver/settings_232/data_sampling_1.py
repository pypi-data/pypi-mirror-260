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

from .data_sampling import data_sampling as data_sampling_cls
from .sampling_interval import sampling_interval as sampling_interval_cls
from .statistics_shear_stress import statistics_shear_stress as statistics_shear_stress_cls
from .statistics_heat_flux import statistics_heat_flux as statistics_heat_flux_cls
from .wall_statistics import wall_statistics as wall_statistics_cls
from .force_statistics import force_statistics as force_statistics_cls
from .time_statistics_dpm import time_statistics_dpm as time_statistics_dpm_cls
from .species_list import species_list as species_list_cls
from .statistics_mixture_fraction import statistics_mixture_fraction as statistics_mixture_fraction_cls
from .statistics_reaction_progress import statistics_reaction_progress as statistics_reaction_progress_cls
from .save_cff_unsteady_statistics import save_cff_unsteady_statistics as save_cff_unsteady_statistics_cls
from .udf_cf_names import udf_cf_names as udf_cf_names_cls
class data_sampling(Group):
    """
    'data_sampling' child.
    """

    fluent_name = "data-sampling"

    child_names = \
        ['data_sampling', 'sampling_interval', 'statistics_shear_stress',
         'statistics_heat_flux', 'wall_statistics', 'force_statistics',
         'time_statistics_dpm', 'species_list', 'statistics_mixture_fraction',
         'statistics_reaction_progress', 'save_cff_unsteady_statistics',
         'udf_cf_names']

    _child_classes = dict(
        data_sampling=data_sampling_cls,
        sampling_interval=sampling_interval_cls,
        statistics_shear_stress=statistics_shear_stress_cls,
        statistics_heat_flux=statistics_heat_flux_cls,
        wall_statistics=wall_statistics_cls,
        force_statistics=force_statistics_cls,
        time_statistics_dpm=time_statistics_dpm_cls,
        species_list=species_list_cls,
        statistics_mixture_fraction=statistics_mixture_fraction_cls,
        statistics_reaction_progress=statistics_reaction_progress_cls,
        save_cff_unsteady_statistics=save_cff_unsteady_statistics_cls,
        udf_cf_names=udf_cf_names_cls,
    )

