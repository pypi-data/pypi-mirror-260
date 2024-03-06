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

class number_of_eulerian_discrete_phases(IntegerList):
    """
    Sets the number of phases, calculated with the Discrete Phase model.
    The sum of Eulerian and Discrete phases has to be in the range (2,20).
    """

    fluent_name = "number-of-eulerian-discrete-phases"

