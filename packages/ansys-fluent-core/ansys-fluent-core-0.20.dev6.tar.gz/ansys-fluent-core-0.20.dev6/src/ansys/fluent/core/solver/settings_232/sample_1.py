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

from .injections_1 import injections as injections_cls
from .boundaries_1 import boundaries as boundaries_cls
from .lines_1 import lines as lines_cls
from .planes import planes as planes_cls
from .op_udf import op_udf as op_udf_cls
from .append_sample import append_sample as append_sample_cls
from .accumulate_rates import accumulate_rates as accumulate_rates_cls
class sample(Command):
    """
    'sample' command.
    
    Parameters
    ----------
        injections : typing.List[str]
            'injections' child.
        boundaries : typing.List[str]
            'boundaries' child.
        lines : typing.List[str]
            'lines' child.
        planes : typing.List[str]
            'planes' child.
        op_udf : str
            'op_udf' child.
        append_sample : bool
            'append_sample' child.
        accumulate_rates : bool
            'accumulate_rates' child.
    
    """

    fluent_name = "sample"

    argument_names = \
        ['injections', 'boundaries', 'lines', 'planes', 'op_udf',
         'append_sample', 'accumulate_rates']

    _child_classes = dict(
        injections=injections_cls,
        boundaries=boundaries_cls,
        lines=lines_cls,
        planes=planes_cls,
        op_udf=op_udf_cls,
        append_sample=append_sample_cls,
        accumulate_rates=accumulate_rates_cls,
    )

