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

from .verbosity_9 import verbosity as verbosity_cls
from .skewness_neighbor_coupling import skewness_neighbor_coupling as skewness_neighbor_coupling_cls
from .hybrid_nita_settings import hybrid_nita_settings as hybrid_nita_settings_cls
class nita_expert_controls(Group):
    """
    Enter the NITA expert controls menu.
    """

    fluent_name = "nita-expert-controls"

    child_names = \
        ['verbosity', 'skewness_neighbor_coupling', 'hybrid_nita_settings']

    _child_classes = dict(
        verbosity=verbosity_cls,
        skewness_neighbor_coupling=skewness_neighbor_coupling_cls,
        hybrid_nita_settings=hybrid_nita_settings_cls,
    )

