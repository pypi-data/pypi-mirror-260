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

from .view_1 import view as view_cls
class stored_view(Command):
    """
    Play the 3D animation sequence using the view stored in the sequence.
    
    Parameters
    ----------
        view : bool
            Yes: "Stored View", no: "Different View".
    
    """

    fluent_name = "stored-view?"

    argument_names = \
        ['view']

    _child_classes = dict(
        view=view_cls,
    )

