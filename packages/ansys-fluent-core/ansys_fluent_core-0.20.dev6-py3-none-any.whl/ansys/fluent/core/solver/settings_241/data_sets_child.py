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

from .zones_3 import zones as zones_cls
from .min_1 import min as min_cls
from .max_1 import max as max_cls
from .mean import mean as mean_cls
from .rmse import rmse as rmse_cls
from .moving_average import moving_average as moving_average_cls
from .average_over_1 import average_over as average_over_cls
class data_sets_child(Group):
    """
    'child_object_type' of data_sets.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['zones', 'min', 'max', 'mean', 'rmse', 'moving_average',
         'average_over']

    _child_classes = dict(
        zones=zones_cls,
        min=min_cls,
        max=max_cls,
        mean=mean_cls,
        rmse=rmse_cls,
        moving_average=moving_average_cls,
        average_over=average_over_cls,
    )

