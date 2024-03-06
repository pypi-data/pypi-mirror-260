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

from .sample_name import sample_name as sample_name_cls
from .interval_size import interval_size as interval_size_cls
class dpm_sample_contour_plots(Command):
    """
    Prepare named expressions from data in a DPM sample file (collected at a cut plane surface) for contour plotting.
    
    Parameters
    ----------
        sample_name : str
            'sample_name' child.
        interval_size : real
            'interval_size' child.
    
    """

    fluent_name = "dpm-sample-contour-plots"

    argument_names = \
        ['sample_name', 'interval_size']

    _child_classes = dict(
        sample_name=sample_name_cls,
        interval_size=interval_size_cls,
    )

