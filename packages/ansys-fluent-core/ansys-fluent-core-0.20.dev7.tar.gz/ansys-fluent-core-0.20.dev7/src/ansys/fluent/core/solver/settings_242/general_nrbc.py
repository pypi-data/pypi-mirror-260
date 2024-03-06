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

from .sigma import sigma as sigma_cls
from .sigma2 import sigma2 as sigma2_cls
from .relax import relax as relax_cls
from .tangential_source import tangential_source as tangential_source_cls
from .verbosity_4 import verbosity as verbosity_cls
class general_nrbc(Group):
    """
    Enter the menu for setting general non-reflecting boundary conditions.
    """

    fluent_name = "general-nrbc"

    child_names = \
        ['sigma', 'sigma2', 'relax', 'tangential_source', 'verbosity']

    _child_classes = dict(
        sigma=sigma_cls,
        sigma2=sigma2_cls,
        relax=relax_cls,
        tangential_source=tangential_source_cls,
        verbosity=verbosity_cls,
    )

