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

class amg_iterations(Integer):
    """
    Number of AMG iterations in each sub-iteration. Increasing the number may improve the overall convergence, but it also increases the time for each sub-iteration.
    """

    fluent_name = "amg-iterations"

