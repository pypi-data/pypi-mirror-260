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

from .zone_names_4 import zone_names as zone_names_cls
from .domain import domain as domain_cls
from .quantities import quantities as quantities_cls
from .min_2 import min as min_cls
from .max_2 import max as max_cls
from .mean_1 import mean as mean_cls
from .rmse_1 import rmse as rmse_cls
from .moving_average_1 import moving_average as moving_average_cls
from .average_over import average_over as average_over_cls
class add_datasets(Command):
    """
    Add datasets.
    
    Parameters
    ----------
        zone_names : typing.List[str]
            Enter zone name list.
        domain : str
            'domain' child.
        quantities : typing.List[str]
            'quantities' child.
        min : bool
            'min' child.
        max : bool
            'max' child.
        mean : bool
            'mean' child.
        rmse : bool
            'rmse' child.
        moving_average : bool
            'moving_average' child.
        average_over : int
            'average_over' child.
    
    """

    fluent_name = "add-datasets"

    argument_names = \
        ['zone_names', 'domain', 'quantities', 'min', 'max', 'mean', 'rmse',
         'moving_average', 'average_over']

    _child_classes = dict(
        zone_names=zone_names_cls,
        domain=domain_cls,
        quantities=quantities_cls,
        min=min_cls,
        max=max_cls,
        mean=mean_cls,
        rmse=rmse_cls,
        moving_average=moving_average_cls,
        average_over=average_over_cls,
    )

