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

class verbosity(Integer):
    """
    Set turbo-specific non-reflecting b.c. verbosity level.
     0 : silent
     1 : basic info. default 
     2 : detailed info. for debugging .
    """

    fluent_name = "verbosity"

