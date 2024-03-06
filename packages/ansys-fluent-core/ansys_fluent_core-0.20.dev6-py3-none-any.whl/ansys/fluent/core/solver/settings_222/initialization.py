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

from .fmg_initialize import fmg_initialize as fmg_initialize_cls
from .localized_turb_init import localized_turb_init as localized_turb_init_cls
from .reference_frame_1 import reference_frame as reference_frame_cls
from .fmg_options import fmg_options as fmg_options_cls
from .set_hybrid_init_options import set_hybrid_init_options as set_hybrid_init_options_cls
from .patch import patch as patch_cls
from .standard_initialize import standard_initialize as standard_initialize_cls
from .hybrid_initialize import hybrid_initialize as hybrid_initialize_cls
from .dpm_reset import dpm_reset as dpm_reset_cls
from .lwf_reset import lwf_reset as lwf_reset_cls
from .init_flow_statistics import init_flow_statistics as init_flow_statistics_cls
from .init_acoustics_options import init_acoustics_options as init_acoustics_options_cls
class initialization(Group):
    """
    'initialization' child.
    """

    fluent_name = "initialization"

    child_names = \
        ['fmg_initialize', 'localized_turb_init', 'reference_frame',
         'fmg_options', 'set_hybrid_init_options', 'patch']

    command_names = \
        ['standard_initialize', 'hybrid_initialize', 'dpm_reset', 'lwf_reset',
         'init_flow_statistics', 'init_acoustics_options']

    _child_classes = dict(
        fmg_initialize=fmg_initialize_cls,
        localized_turb_init=localized_turb_init_cls,
        reference_frame=reference_frame_cls,
        fmg_options=fmg_options_cls,
        set_hybrid_init_options=set_hybrid_init_options_cls,
        patch=patch_cls,
        standard_initialize=standard_initialize_cls,
        hybrid_initialize=hybrid_initialize_cls,
        dpm_reset=dpm_reset_cls,
        lwf_reset=lwf_reset_cls,
        init_flow_statistics=init_flow_statistics_cls,
        init_acoustics_options=init_acoustics_options_cls,
    )

