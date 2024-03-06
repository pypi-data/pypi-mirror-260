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
class enable_strategy(Command):
    """
    Specify whether automatic initialization and case modification should be enabled.
    
    Parameters
    ----------
        enable : bool
            'enable' child.
    
    """

    fluent_name = "enable-strategy?"

    argument_names = \
        ['enable']

    _child_classes = dict(
        enable=enable_cls,
    )

