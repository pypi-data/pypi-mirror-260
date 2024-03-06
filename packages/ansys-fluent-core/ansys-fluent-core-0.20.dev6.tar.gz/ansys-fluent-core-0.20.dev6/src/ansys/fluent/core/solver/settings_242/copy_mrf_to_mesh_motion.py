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

from .zone_name_1 import zone_name as zone_name_cls
from .overwrite import overwrite as overwrite_cls
class copy_mrf_to_mesh_motion(Command):
    """
    Copy motion variable values for origin, axis and velocities from Frame Motion to Mesh Motion.
    
    Parameters
    ----------
        zone_name : str
            Enter a zone name.
        overwrite : bool
            Specify if you want to overwrite the motion variables.
    
    """

    fluent_name = "copy-mrf-to-mesh-motion"

    argument_names = \
        ['zone_name', 'overwrite']

    _child_classes = dict(
        zone_name=zone_name_cls,
        overwrite=overwrite_cls,
    )

