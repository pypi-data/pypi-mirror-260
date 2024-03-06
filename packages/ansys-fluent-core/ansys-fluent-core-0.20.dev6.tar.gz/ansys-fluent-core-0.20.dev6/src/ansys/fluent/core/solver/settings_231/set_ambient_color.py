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

from .rgb_vector import rgb_vector as rgb_vector_cls
class set_ambient_color(Command):
    """
    'set_ambient_color' command.
    
    Parameters
    ----------
        rgb_vector : typing.Tuple[real, real, real]
            'rgb_vector' child.
    
    """

    fluent_name = "set-ambient-color"

    argument_names = \
        ['rgb_vector']

    _child_classes = dict(
        rgb_vector=rgb_vector_cls,
    )

