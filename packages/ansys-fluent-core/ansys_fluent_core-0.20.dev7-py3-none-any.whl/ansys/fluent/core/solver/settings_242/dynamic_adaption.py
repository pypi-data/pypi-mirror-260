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

from .enable import enable as enable_cls
class dynamic_adaption(Command):
    """
    Adapt the mesh during solution.
    
    Parameters
    ----------
        enable : bool
            'enable' child.
    
    """

    fluent_name = "dynamic-adaption?"

    argument_names = \
        ['enable']

    _child_classes = dict(
        enable=enable_cls,
    )

