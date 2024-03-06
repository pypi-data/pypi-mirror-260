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

from .side_1 import side_1 as side_1_cls
from .side_2 import side_2 as side_2_cls
from .angle_2 import angle as angle_cls
from .interface_name_1 import interface_name as interface_name_cls
class make_phaselag_from_boundaries(Command):
    """
    Make interface zones phase lagged.
    
    Parameters
    ----------
        side_1 : str
            Enter id/name of zone to convert to phase lag side 1.
        side_2 : str
            Enter id/name of zone to convert to phase lag side 2.
        angle : real
            Enter rotation angle.
        interface_name : str
            Enter a name for this phaselag interface.
    
    """

    fluent_name = "make-phaselag-from-boundaries"

    argument_names = \
        ['side_1', 'side_2', 'angle', 'interface_name']

    _child_classes = dict(
        side_1=side_1_cls,
        side_2=side_2_cls,
        angle=angle_cls,
        interface_name=interface_name_cls,
    )

