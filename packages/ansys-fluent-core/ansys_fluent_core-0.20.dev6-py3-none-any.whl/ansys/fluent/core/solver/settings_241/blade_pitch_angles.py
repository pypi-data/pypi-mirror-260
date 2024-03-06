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

from .blade_pitch_collective import blade_pitch_collective as blade_pitch_collective_cls
from .blade_pitch_cyclic_sin import blade_pitch_cyclic_sin as blade_pitch_cyclic_sin_cls
from .blade_pitch_cyclic_cos import blade_pitch_cyclic_cos as blade_pitch_cyclic_cos_cls
class blade_pitch_angles(Group):
    """
    Menu to define the rotor pitch and flapping angles.
    
     - blade-pitch-collective    : , 
     - blade-pitch-cyclic-sin    : , 
     - blade-pitch-cyclic-cos    : , 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "blade-pitch-angles"

    child_names = \
        ['blade_pitch_collective', 'blade_pitch_cyclic_sin',
         'blade_pitch_cyclic_cos']

    _child_classes = dict(
        blade_pitch_collective=blade_pitch_collective_cls,
        blade_pitch_cyclic_sin=blade_pitch_cyclic_sin_cls,
        blade_pitch_cyclic_cos=blade_pitch_cyclic_cos_cls,
    )

