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

from .contact_resistance import contact_resistance as contact_resistance_cls
from .orthotropic_k import orthotropic_k as orthotropic_k_cls
from .thermal_abuse_model import thermal_abuse_model as thermal_abuse_model_cls
from .capacity_fade_model import capacity_fade_model as capacity_fade_model_cls
from .life_model import life_model as life_model_cls
from .swelling_model import swelling_model as swelling_model_cls
from .venting_model import venting_model as venting_model_cls
from .udf_hooks import udf_hooks as udf_hooks_cls
class advanced_models(Group):
    """
    Advanced model options.
    """

    fluent_name = "advanced-models"

    child_names = \
        ['contact_resistance', 'orthotropic_k', 'thermal_abuse_model',
         'capacity_fade_model', 'life_model', 'swelling_model',
         'venting_model', 'udf_hooks']

    _child_classes = dict(
        contact_resistance=contact_resistance_cls,
        orthotropic_k=orthotropic_k_cls,
        thermal_abuse_model=thermal_abuse_model_cls,
        capacity_fade_model=capacity_fade_model_cls,
        life_model=life_model_cls,
        swelling_model=swelling_model_cls,
        venting_model=venting_model_cls,
        udf_hooks=udf_hooks_cls,
    )

