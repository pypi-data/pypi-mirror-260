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

from .mean_and_std_deviation import mean_and_std_deviation as mean_and_std_deviation_cls
from .pb_disc_components import pb_disc_components as pb_disc_components_cls
class pb_disc(Group):
    """
    Help not available.
    """

    fluent_name = "pb-disc"

    child_names = \
        ['mean_and_std_deviation', 'pb_disc_components']

    _child_classes = dict(
        mean_and_std_deviation=mean_and_std_deviation_cls,
        pb_disc_components=pb_disc_components_cls,
    )

