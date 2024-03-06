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

from .crossflow_transition import crossflow_transition as crossflow_transition_cls
from .critical_reynolds_number_correlation import critical_reynolds_number_correlation as critical_reynolds_number_correlation_cls
from .clambda_scale import clambda_scale as clambda_scale_cls
from .capg_hightu import capg_hightu as capg_hightu_cls
from .cfpg_hightu import cfpg_hightu as cfpg_hightu_cls
from .capg_lowtu import capg_lowtu as capg_lowtu_cls
from .cfpg_lowtu import cfpg_lowtu as cfpg_lowtu_cls
from .ctu_hightu import ctu_hightu as ctu_hightu_cls
from .ctu_lowtu import ctu_lowtu as ctu_lowtu_cls
from .rec_max import rec_max as rec_max_cls
from .rec_c1 import rec_c1 as rec_c1_cls
from .rec_c2 import rec_c2 as rec_c2_cls
from .cbubble_c1 import cbubble_c1 as cbubble_c1_cls
from .cbubble_c2 import cbubble_c2 as cbubble_c2_cls
from .rv1_switch import rv1_switch as rv1_switch_cls
class transition_model_options(Group):
    """
    'transition_model_options' child.
    """

    fluent_name = "transition-model-options"

    child_names = \
        ['crossflow_transition', 'critical_reynolds_number_correlation',
         'clambda_scale', 'capg_hightu', 'cfpg_hightu', 'capg_lowtu',
         'cfpg_lowtu', 'ctu_hightu', 'ctu_lowtu', 'rec_max', 'rec_c1',
         'rec_c2', 'cbubble_c1', 'cbubble_c2', 'rv1_switch']

    _child_classes = dict(
        crossflow_transition=crossflow_transition_cls,
        critical_reynolds_number_correlation=critical_reynolds_number_correlation_cls,
        clambda_scale=clambda_scale_cls,
        capg_hightu=capg_hightu_cls,
        cfpg_hightu=cfpg_hightu_cls,
        capg_lowtu=capg_lowtu_cls,
        cfpg_lowtu=cfpg_lowtu_cls,
        ctu_hightu=ctu_hightu_cls,
        ctu_lowtu=ctu_lowtu_cls,
        rec_max=rec_max_cls,
        rec_c1=rec_c1_cls,
        rec_c2=rec_c2_cls,
        cbubble_c1=cbubble_c1_cls,
        cbubble_c2=cbubble_c2_cls,
        rv1_switch=rv1_switch_cls,
    )

