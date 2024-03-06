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

from .permeation_enabled import permeation_enabled as permeation_enabled_cls
from .permeation_n import permeation_n as permeation_n_cls
from .permeation_name import permeation_name as permeation_name_cls
from .permeation_rate import permeation_rate as permeation_rate_cls
from .permeation_ea import permeation_ea as permeation_ea_cls
class species_permeation(Group):
    """
    Set up species permeation.
    """

    fluent_name = "species-permeation"

    child_names = \
        ['permeation_enabled', 'permeation_n', 'permeation_name',
         'permeation_rate', 'permeation_ea']

    _child_classes = dict(
        permeation_enabled=permeation_enabled_cls,
        permeation_n=permeation_n_cls,
        permeation_name=permeation_name_cls,
        permeation_rate=permeation_rate_cls,
        permeation_ea=permeation_ea_cls,
    )

