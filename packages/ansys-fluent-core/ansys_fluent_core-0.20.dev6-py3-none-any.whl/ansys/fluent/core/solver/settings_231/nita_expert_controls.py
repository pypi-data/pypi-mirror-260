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

from .set_verbosity import set_verbosity as set_verbosity_cls
from .skewness_neighbor_coupling_1 import skewness_neighbor_coupling as skewness_neighbor_coupling_cls
from .hybrid_nita_settings import hybrid_nita_settings as hybrid_nita_settings_cls
class nita_expert_controls(Group):
    """
    Enter the nita expert controls menu.
    """

    fluent_name = "nita-expert-controls"

    child_names = \
        ['set_verbosity', 'skewness_neighbor_coupling',
         'hybrid_nita_settings']

    _child_classes = dict(
        set_verbosity=set_verbosity_cls,
        skewness_neighbor_coupling=skewness_neighbor_coupling_cls,
        hybrid_nita_settings=hybrid_nita_settings_cls,
    )

