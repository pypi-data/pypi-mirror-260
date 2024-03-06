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

from .factor import factor as factor_cls
class zoom(Command):
    """
    Adjust the camera field of view.
    
    Parameters
    ----------
        factor : real
            'factor' child.
    
    """

    fluent_name = "zoom"

    argument_names = \
        ['factor']

    _child_classes = dict(
        factor=factor_cls,
    )

