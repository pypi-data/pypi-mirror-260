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

class trim_option(Integer):
    """
    Select Trimming Option:
    
     - Enter 0 if no trimming is required 
     - Enter 1 if trimming of collective pitch is required 
     - Enter 2 if trimming of cyclic pitch angles are required 
     - Enter 3 if trimming of both collective and cyclic pitch angles are required 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "trim-option"

