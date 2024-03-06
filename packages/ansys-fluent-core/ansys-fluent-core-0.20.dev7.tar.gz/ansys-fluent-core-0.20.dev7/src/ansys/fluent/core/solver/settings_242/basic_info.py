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

from .number_of_blades import number_of_blades as number_of_blades_cls
from .rotor_speed import rotor_speed as rotor_speed_cls
from .tip_radius import tip_radius as tip_radius_cls
from .root_radius import root_radius as root_radius_cls
class basic_info(Group):
    """
    Menu to define the rotor basic informations:
    
     - Number of Blades 
     - Rotor Speed  , 
     - Tip Radius 
     - Root Radius , 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "basic-info"

    child_names = \
        ['number_of_blades', 'rotor_speed', 'tip_radius', 'root_radius']

    _child_classes = dict(
        number_of_blades=number_of_blades_cls,
        rotor_speed=rotor_speed_cls,
        tip_radius=tip_radius_cls,
        root_radius=root_radius_cls,
    )

